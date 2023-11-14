from flask import Flask, request, g, session, jsonify, render_template, make_response

from flask_migrate import Migrate
from models import db, Production, CrewMember

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

migrate = Migrate(app, db)
db.init_app(app)

# from werkzeug.exceptions import BadRequest, InternalServerError


# @app.errorhandler(BadRequest)  # 400
# def handle_bad_request(error):
#     response = jsonify({"message": "Bad Request"})
#     response.status_code = error.code
#     return response


@app.route("/")
def welcome():
    return render_template("home.html", test=False)


@app.route("/productions", methods=["GET", "POST"])
def productions():
    if request.method == "GET":
        prods = [
            prod.as_dict() for prod in Production.query.all()
        ]
        return prods, 200
        # return jsonify(prods), 200
        # return make_response(prods, 200)
    else:
        try:
            data = request.get_json()
            prod = Production(**data)
            db.session.add(prod)
            db.session.commit()
            return prod.as_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400
