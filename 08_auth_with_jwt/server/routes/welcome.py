from flask_restful import Resource
from flask import make_response, render_template

class Welcome(Resource):
    def get(self):
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("home.html"), 200, headers)
        # return render_template("home.html", test=False)
