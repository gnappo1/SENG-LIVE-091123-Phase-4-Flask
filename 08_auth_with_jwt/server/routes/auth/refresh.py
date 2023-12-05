from flask_restful import Resource
from flask import jsonify, make_response
from flask_jwt_extended import (
    jwt_required,
    current_user,
    create_access_token,
    set_access_cookies,
    get_jwt_identity,
)
from app_setup import db
from schemas.user_schema import UserSchema

user_schema = UserSchema(session=db.session)


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            jwt = create_access_token(identity=get_jwt_identity())
            return make_response({"user": user_schema.dump(current_user), "jwt_token": jwt}, 200)
        except Exception as e:
            return {"message": str(e)}, 400