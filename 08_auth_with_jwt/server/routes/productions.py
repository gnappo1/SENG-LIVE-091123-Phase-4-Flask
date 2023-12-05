from flask import request, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask_jwt_extended import (
    jwt_required,
)
from app_setup import db
from models.production import Production
from schemas.production_schema import ProductionSchema

production_schema = ProductionSchema(session=db.session)
productions_schema = ProductionSchema(
    many=True, exclude=("crew_members",), session=db.session
)


class Productions(Resource):
    def get(self):
        prods = productions_schema.dump(Production.query)
        #! example of using cookies -> not needed for app reasons
        #! will stay there until unset!
        return prods, 200

    @jwt_required()
    def post(self):
        try:
            # * Extract data out of the request
            data = request.get_json()
            # * Validate the data, if problems arise you'll see ValidationError
            production_schema.validate(data)
            # * Deserialize the data with dump()
            prod = production_schema.load(data)
            db.session.add(prod)
            db.session.commit()
            # * Serialize the data and package your JSON response
            serialized_product = production_schema.dump(prod)
            return serialized_product, 201
        except (ValidationError, ValueError, IntegrityError) as e:
            db.session.rollback()
            abort(400, str(e))
