from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
from sqlalchemy.exc import IntegrityError
from app_setup import db
from schemas.user_schema import UserSchema

user_schema = UserSchema(session=db.session)


class Signup(Resource):
    def post(self):
        try:
            # * Extract data out of the request
            data = {
                "email": request.get_json().get("email"),
                "username": request.get_json().get("username"),
            }
            # * Validate the data, if problems arise you'll see ValidationError
            user_schema.validate(data)
            # * Deserialize the data with dump()
            user = user_schema.load(data)
            user.password_hash = request.get_json().get("password")
            db.session.add(user)
            db.session.commit()
            #! new code for JWT
            jwt = create_access_token(identity=user.id)
            #! manually set a refresh token
            refresh_token = create_refresh_token(identity=user.id)
            #! serialize the user
            serialized_user = user_schema.dump(user)
            #! ready to send the response!
            return make_response({"user": serialized_user, "jwt_token": jwt, "refresh_token": refresh_token}, 201)
        except (Exception, IntegrityError) as e:
            db.session.rollback()
            return {"message": str(e)}, 400
