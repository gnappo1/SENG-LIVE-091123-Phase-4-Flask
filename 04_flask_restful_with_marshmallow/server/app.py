#!/usr/bin/env python3

#! 📚 Review With Students:
# API Fundamentals
# MVC Architecture and Patterns / Best Practices
# RESTful Routing
# Serialization
# Postman

#! Set Up When starting from scratch:
# In Terminal, `cd` into `server` and run the following:
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db migrate -m 'Create tables'
# flask db upgrade
# python seed.py


from flask import (
    Flask,
    request,
    g,
    session,
    jsonify,
    render_template,
    make_response,
    abort,
)
from flask_migrate import Migrate
from models import db, Production, CrewMember
from werkzeug.exceptions import NotFound
from time import time
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from marshmallow import fields, validates, validate, ValidationError

#! App creation and configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

#! flask-migrate setup
migrate = Migrate(app, db)
#! flask-sqlalchemy setup
db.init_app(app)
ma = Marshmallow(app)
api = Api(app, prefix="/api/v1")


class CrewMemberSchema(ma.SQLAlchemySchema):
    class Meta:
        # name of model
        model = CrewMember
        # avoid recreating objects on updates, only applies to deserialization (load())
        # in order for this to work, flask-marshmallow (is specific to this wrapper)
        # needs to know how an instance even looks like, note how we invoked load() on line 222
        load_instance = True
        #  if you set to True, Marshmallow will preserve the order of fields as defined in the schema.
        ordered = True
        # Specify which fields to serialize (not deserialize)
        fields = ("id", "name", "role", "production_id", "production", "url")

    #! Setup some app-level (aka no DB involved) validations
    # * See more here https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#module-marshmallow.validate
    name = fields.String(required=True)
    production = fields.Nested("ProductionSchema", exclude=("crew_members",))
    production_id = fields.Integer(required=True)
    role = fields.String(
        required=True,
        validate=validate.Length(
            min=3,
            max=50,
            error="Role should be a string at least 3 chars long! But max 50!",
        ),
    )

    #! Create hyperlinks for easy navigation of your api
    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("crewmemberbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("crewmembers"),
        }
    )

    #! Example of custom validation with marshmallow
    #! (DANGER -> VERY similar to the syntax in the models)
    @validates("name")
    def validate_word_count(self, name):
        words = name.split()
        if len(words) < 2:
            raise ValidationError("Text must contain at least two words")


#! Create schema for a single crew_member
crew_member_schema = CrewMemberSchema()
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize
crew_members_schema = CrewMemberSchema(many=True)


class ProductionSchema(ma.SQLAlchemySchema):
    #! The notes are the same as above in CrewMemberSchema ^^^
    class Meta:
        model = Production
        load_instance = True
        fields = (
            "title",
            "genre",
            "budget",
            "director",
            "description",
            "id",
            "image",
            "ongoing",
            "crew_members",
            "url",
        )

    crew_members = fields.Nested(
        "CrewMemberSchema",
        only=("id", "name", "role"),
        exclude=("production",),
        many=True,
    )
    title = fields.String(required=True, validate=validate.Length(min=2, max=50))
    director = fields.String(required=True, validate=validate.Length(min=2, max=50))
    description = fields.String(
        required=True, validate=validate.Length(min=30, max=500)
    )
    genre = fields.String(required=True, validate=validate.Length(min=2, max=50))
    image = fields.String(
        required=True,
        validate=validate.Regexp(
            r".*\.(jpeg|png)", error="File URI must be in JPEG or PNG format"
        ),
    )
    budget = fields.Float(
        required=True, validate=validate.Range(min=0.99, max=500000000)
    )

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("productionbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("productions"),
            "crewmembers": ma.URLFor("crewmembers"),
        }
    )


#! Create schema for a single crew_member
production_schema = ProductionSchema()
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize
productions_schema = ProductionSchema(many=True, exclude=("crew_members",))


#! Global Error Handling
@app.errorhandler(NotFound)  #! 404
def handle_404(error):
    response = {"message": error.description}
    return response, error.code


#! Routes
# @app.route("/")
class Welcome(Resource):
    def get(self):
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("home.html", test=False), 200, headers)
        # return render_template("home.html", test=False)


api.add_resource(Welcome, "/")


@app.before_request
def before_request():
    g.time = time()


@app.after_request
def after_request(response):
    diff = time() - g.time
    print(f"Request took {diff} seconds")
    response.headers["X-Response-Time"] = str(diff)
    return response


#! GET/POST Productions routes
class Productions(Resource):
    def get(self):
        prods = productions_schema.dump(Production.query)
        return prods

    def post(self):
        try:
            # * Extract data out of the request
            data = request.get_json()
            # * Validate the data, if problems arise you'll see ValidationError
            production_schema.validate(data)
            # * Deserialize the data with dump()
            prod = production_schema.load(data)
            db.session.add(prod)
            db.session.commit()
            # * Serialize the data and package your JSON response
            serialized_product = production_schema.dump(prod)
            return serialized_product, 201
        except (ValidationError, ValueError, IntegrityError) as e:
            db.session.rollback()
            abort(400, str(e))


api.add_resource(Productions, "/productions")


#! GET/PATCH/DELETE Production routes
class ProductionById(Resource):
    def get(self, id):
        prod = Production.query.get_or_404(
            id, description=f"Could not find production with id: {id}"
        )
        try:
            serialized_data = production_schema.dump(prod)
            return serialized_data, 200
        except Exception as e:
            abort(400, str(e))

    def patch(self, id):
        prod = Production.query.get_or_404(
            id, description=f"Could not find production with id: {id}"
        )
        try:
            data = request.get_json()
            # * Validate the data, if problems arise you'll see ValidationError
            production_schema.validate(data)
            # * partial = True allows partial updates, meaning only the provided fields
            # * in the JSON data will be updated, and the rest will remain unchanged.
            # * Remember what we said about passing the instance to load() in order
            # * for marshmallow to reuse an existing object rather than recreating one?
            updated_prod = production_schema.load(data, instance=prod, partial=True)
            db.session.commit()
            #! pre-marshmallow code
            # for attr_name, attr_value in data.items():
            #     setattr(prod, attr_name, attr_value)
            #! title will be null just because the @validates forgot to return
            return production_schema.dump(updated_prod), 200
        except (ValueError, ValidationError, IntegrityError) as e:
            db.session.rollback()
            abort(400, str(e))

    def delete(self, id):
        prod = Production.query.get_or_404(
            id, description=f"Could not find production with id: {id}"
        )
        try:
            db.session.delete(prod)
            db.session.commit()
            return None, 204
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))


api.add_resource(ProductionById, "/productions/<int:id>")


#! GET/POST CrewMembers routes
class CrewMembers(Resource):
    def get(self):
        crew = crew_members_schema.dump(CrewMember.query)
        return crew, 200

    def post(self):
        try:
            data = request.json
            # * Validate the data, if problems arise you'll see ValidationError
            crew_member_schema.validate(data)
            # * Deserialize the data with dump()
            crew = crew_member_schema.load(data)
            db.session.add(crew)
            db.session.commit()
            # * Serialize the data and package your JSON response
            serialized_crew = crew_member_schema.dump(crew)
            return serialized_crew, 201
        except (ValidationError, ValueError) as e:
            db.session.rollback()
            abort(400, str(e))


api.add_resource(CrewMembers, "/crew_members")

#! GET/PATCH/DELETE CrewMembers routes


class CrewMemberById(Resource):
    def get(self, id):
        cm = CrewMember.query.get_or_404(
            id, description=f"Could not find crew_member with id: {id}"
        )
        return crew_member_schema.dump(cm), 200

    def patch(self, id):
        cm = CrewMember.query.get_or_404(
            id, description=f"Could not find crew_member with id: {id}"
        )
        try:
            data = request.get_json()
            crew_member_schema.validate(data)
            updated_crew = crew_member_schema.load(data, instance=cm, partial=True)
            #! pre-marshmallow logic
            # for attr_name, attr_value in data.items():
            #     setattr(cm, attr_name, attr_value)
            db.session.commit()
            return crew_member_schema.dump(updated_crew), 200
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    def delete(self, id):
        cm = CrewMember.query.get_or_404(
            id, description=f"Could not find crew_member with id: {id}"
        )
        try:
            db.session.delete(cm)
            db.session.commit()
            return None, 204
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))


api.add_resource(CrewMemberById, "/crew_members/<int:id>")

if __name__ == "__main__":
    app.run(debug=True, port=5555)
