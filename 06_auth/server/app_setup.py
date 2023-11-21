from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")

#! flask-sqlalchemy setup
db = SQLAlchemy(app)
#! flask-migrate setup
migrate = Migrate(app, db)
#! flask-marshmallow setup
ma = Marshmallow(app)
#! flask-bcrypt setup
bcrypt = Bcrypt(app)
#! flask-restful setup
api = Api(app, prefix="/api/v1")
