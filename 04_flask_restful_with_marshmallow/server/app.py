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
        self.parser.add_argument("title", type=str, required=True, help="Title must be present!")
        self.parser.add_argument("genre", type=str, required=True, help="Genre must be present!")
        self.parser.add_argument(
            "description", type=str, required=True, help="Description must be present!"
        )
        self.parser.add_argument(
            "director", type=str, required=True, help="Director must be present!"
        )
        self.parser.add_argument("image", type=str, required=True, help="Image must be present!")
        self.parser.add_argument("budget", type=float, required=True, help="Budget must be present!")
        self.parser.add_argument(
            "ongoing", type=bool, required=True, help="Ongoing must be present!"
        )

#! Global Error Handling
@app.errorhandler(NotFound)  #! 404
def handle_404(error):
    response = jsonify({"error": error.description})
    response.status_code = error.code
    return response

#! Routes
@app.route("/")
def welcome():
    return render_template("home.html", test=False)

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
        prods = [prod.to_dict(only=("id",)) for prod in Production.query.all()]
        return prods

    def post(self):
        try:
            parser = ParserMixin()
            data = parser.parser.parse_args() #! 10 points for Danner
            prod = Production(**data)
            db.session.add(prod)
            db.session.commit()
            return prod.to_dict(), 201
        except IntegrityError as e:
            db.session.rollback()
            return {"error": str(e)}, 400
        except AttributeError as e:
            db.session.rollback()
            return {"error": str(e)}, 400

api.add_resource(Productions, "/productions")

class ProductionById(Resource):
    def get(self, id):
        if prod := db.session.get(Production, id):
            return prod.as_dict(), 200
        abort(404, f"Could not find Production with id {id}")

api.add_resource(ProductionById, "/productions/<int:id>")

if __name__ == "__main__":
    app.run(debug=True, port=5555)
