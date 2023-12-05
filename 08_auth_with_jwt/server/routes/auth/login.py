from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
from app_setup import db
from models.user import User
from schemas.user_schema import UserSchema

user_schema = UserSchema(session=db.session)


class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            user = User.query.filter_by(email=data.get("email")).first()
            # if yes: now onto validating password -> if yes: send the serialized user to frontend
            if user and user.authenticate(data.get("password")):
                #! new code for jwt
                jwt = create_access_token(identity=user.id)
                #! manually set a refresh token
                refresh_token = create_refresh_token(identity=user.id)
                #! serialize the user
                serialized_user = user_schema.dump(user)
                #! ready to send the response!
                return make_response({"user": serialized_user, "jwt_token": jwt, "refresh_token": refresh_token}, 200)
            return {"message": "Invalid Credentials"}, 403
        except Exception as e:
            return {"message": "Invalid Credentials"}, 403
