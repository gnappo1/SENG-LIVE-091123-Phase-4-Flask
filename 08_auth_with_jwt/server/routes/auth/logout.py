from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    unset_access_cookies,
    unset_refresh_cookies,
)


class Logout(Resource):
    def delete(self):
        # del session["user_id"]
        response = make_response({}, 204)
        unset_access_cookies(response)
        unset_refresh_cookies(response)
        return response
