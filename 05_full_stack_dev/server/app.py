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
    render_template,
    make_response,
    abort,
    current_app,
)
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from time import time
from marshmallow import ValidationError

from models.crew_member import CrewMember
from models.production import Production
from app_setup import app, api, db


def main():
    #! App creation and configuration
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    #! flask-migrate setup
    migrate = Migrate(app, db)
    #! flask-sqlalchemy setup
    db.init_app(app)
    api = Api(app, prefix="/api/v1")

    return (app, api, db)


from schemas.crew_member_schema import CrewMemberSchema
from schemas.production_schema import ProductionSchema

#! Marshmallow Schemas
#! Create schema for a single crew_member
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize

#! Create schema for a single crew_member
#! Create schema for a collection of crew_members
# * Feel free to use only and exclude to customize


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
        productions_schema = ProductionSchema(many=True, exclude=("crew_members",))
        prods = productions_schema.dump(Production.query)
        return prods

    def post(self):
        try:
            # * Extract data out of the request
            data = request.get_json()
            production_schema = ProductionSchema()
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
            production_schema = ProductionSchema()
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
            production_schema = ProductionSchema()
            # * Validate the data, if problems arise you'll see ValidationError
            production_schema.validate(data)
            # * partial = True allows partial updates, meaning only the provided fields
            # * in the JSON data will be updated, and the rest will remain unchanged.
            # * Remember what we said about passing the instance to load() in order
            # * for marshmallow to reuse an existing object rather than recreating one?
            updated_prod = production_schema.load(
                data, session=db.session, instance=prod, partial=True
            )
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
        crew_members_schema = CrewMemberSchema(many=True)
        crew = crew_members_schema.dump(CrewMember.query)
        return crew, 200

    def post(self):
        try:
            data = request.json
            # * Validate the data, if problems arise you'll see ValidationError
            crew_member_schema = CrewMemberSchema()
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
        crew_member_schema = CrewMemberSchema()
        return crew_member_schema.dump(cm), 200

    def patch(self, id):
        cm = CrewMember.query.get_or_404(
            id, description=f"Could not find crew_member with id: {id}"
        )
        try:
            data = request.get_json()
            crew_member_schema = CrewMemberSchema()
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
