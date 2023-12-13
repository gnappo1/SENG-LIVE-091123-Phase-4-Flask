from flask import request, abort
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from app_setup import db
from models.crew_member import CrewMember
from schemas.crew_member_schema import CrewMemberSchema

crew_members_schema = CrewMemberSchema(many=True, session=db.session)
crew_member_schema = CrewMemberSchema(session=db.session)


class CrewMembers(Resource):
    def get(self):
        crew = crew_members_schema.dump(CrewMember.query)
        return crew, 200

    @jwt_required()
    def post(self):
        try:
            data = request.json
            # * Validate the data, if problems arise you'll see ValidationError
            crew_member_schema.validate(data)
            # * Deserialize the data with load()
            crew = crew_member_schema.load(data)
            db.session.add(crew)
            db.session.commit()
            # * Serialize the data and package your JSON response
            serialized_crew = crew_member_schema.dump(crew)
            return serialized_crew, 201
        except (ValidationError, ValueError) as e:
            db.session.rollback()
            abort(400, str(e))
