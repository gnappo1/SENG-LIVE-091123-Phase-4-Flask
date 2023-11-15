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


from flask import Flask, request, g, session, jsonify, render_template, make_response

from flask_migrate import Migrate
from models import db, Production, CrewMember

#! App creation and configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

#! flask-migrate setup
migrate = Migrate(app, db)
#! flask-sqlalchemy setup
db.init_app(app)


#! Routes
@app.route("/")
def welcome():
    return render_template("home.html", test=False)


@app.route("/productions", methods=["GET", "POST"])
def productions():
    if request.method == "GET":
        prods = [prod.as_dict() for prod in Production.query.all()]
        return prods, 200
    else:
        try:
            data = request.get_json()
            prod = Production(**data)
            db.session.add(prod)
            db.session.commit()
            return prod.as_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(debug=True, port=5555)