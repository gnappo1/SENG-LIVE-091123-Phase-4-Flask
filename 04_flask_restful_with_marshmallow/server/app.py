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


class ParserMixin:
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "title", type=str, required=True, help="Title must be present!"
        )
        self.parser.add_argument(
            "genre", type=str, required=True, help="Genre must be present!"
        )
        self.parser.add_argument(
            "description", type=str, required=True, help="Description must be present!"
        )
        self.parser.add_argument(
            "director", type=str, required=True, help="Director must be present!"
        )
        self.parser.add_argument(
            "image", type=str, required=True, help="Image must be present!"
        )
        self.parser.add_argument(
            "budget", type=float, required=True, help="Budget must be present!"
        )
        self.parser.add_argument(
            "ongoing", type=bool, required=True, help="Ongoing must be present!"
        )


#! Global Error Handling
# @app.errorhandler(NotFound)  #! 404
# def handle_404(error):
#     response = jsonify({"error": error.description})
#     response.status_code = error.code
#     return response


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


class Productions(Resource):
    def get(self):
        prods = [prod.to_dict() for prod in Production.query.all()]
        return prods

    def post(self):
        try:
            parser = ParserMixin()
            data = parser.parser.parse_args()
            prod = Production(**data)
            db.session.add(prod)
            db.session.commit()
            return prod.to_dict(), 201
        except (IntegrityError, AttributeError) as e:
            db.session.rollback()
            return {"error": str(e)}, 400


api.add_resource(Productions, "/productions")


class ProductionById(Resource):
    def get(self, id):
        import ipdb; ipdb.set_trace()
        prod = Production.query.get_or_404(id)
        return prod.to_dict(), 200

    def patch(self, id):
        prod = Production.query.get_or_404(id)
        try:
            # parser = ParserMixin()
            # data = parser.parser.parse_args()
            data = request.get_json()
            for attr_name, attr_value in data.items():
                setattr(prod, attr_name, attr_value)
            #! title will be null just because the @validates forgot to return
            db.session.commit()
            return prod.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def delete(self, id):
        prod = Production.query.get_or_404(id)
        try:
            db.session.delete(prod)
            db.session.commit()
            return None, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


api.add_resource(ProductionById, "/productions/<int:id>")


class CrewMemberById(Resource):
    def get(self, id):
        cm = CrewMember.query.get_or_404(id)
        return cm.to_dict(), 200

    def patch(self, id):
        cm = CrewMember.query.get_or_404(id)
        try:
            # parser = ParserMixin()
            # data = parser.parser.parse_args()
            data = request.get_json()
            for attr_name, attr_value in data.items():
                setattr(cm, attr_name, attr_value)
            #! title will be null just because the @validates forgot to return
            db.session.commit()
            return cm.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def delete(self, id):
        cm = CrewMember.query.get_or_404(id)
        try:
            db.session.delete(cm)
            db.session.commit()
            return None, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


api.add_resource(CrewMemberById, "/crew_members/<int:id>")

if __name__ == "__main__":
    app.run(debug=True, port=5555)
