from flask import request, abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app_setup import db
from models.production import Production
from schemas.production_schema import ProductionSchema

production_schema = ProductionSchema(session=db.session)
productions_schema = ProductionSchema(
    many=True, exclude=("crew_members",), session=db.session
)


class ProductionById(Resource):
    def get(self, id):
        prod = Production.query.get_or_404(
            id, description=f"Could not find production with id: {id}"
        )
        try:
            serialized_data = production_schema.dump(prod)
            return serialized_data, 200
        except Exception as e:
            abort(400, str(e))

    @jwt_required()
    def patch(self, id):
        prod = Production.query.get_or_404(
            id, description=f"Could not find production with id: {id}"
        )
        try:
            data = request.get_json()
            production_schema.validate(data)
            updated_prod = production_schema.load(
                data, instance=prod, partial=True, session=db.session
            )
            db.session.commit()
            return production_schema.dump(updated_prod), 200
        except (ValueError, ValidationError, IntegrityError) as e:
            db.session.rollback()
            abort(400, str(e))

    @jwt_required()
    def delete(self, id):
        prod = Production.query.get_or_404(
            id, description=f"Could not find production with id: {id}"
        )
        try:
            db.session.delete(prod)
            db.session.commit()
            return None, 204
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))
