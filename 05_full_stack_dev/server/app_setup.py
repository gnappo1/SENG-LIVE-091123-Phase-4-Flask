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
from models import db
from schemas import ma
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

#! flask-migrate setup
migrate = Migrate(app, db)
#! flask-sqlalchemy setup
db.init_app(app)
ma.init_app(app)
api = Api(app, prefix="/api/v1")