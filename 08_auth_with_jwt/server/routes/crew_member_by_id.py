from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from app_setup import db
from models.crew_member import CrewMember
from schemas.crew_member_schema import CrewMemberSchema

crew_members_schema = CrewMemberSchema(many=True, session=db.session)
crew_member_schema = CrewMemberSchema(session=db.session)


class CrewMemberById(Resource):
    def get(self, id):
        cm = CrewMember.query.get_or_404(
            id, description=f"Could not find crew_member with id: {id}"
        )
        crew_member_schema = CrewMemberSchema()
        return crew_member_schema.dump(cm), 200

    @jwt_required()
    def patch(self, id):
        cm = CrewMember.query.get_or_404(
            id, description=f"Could not find crew_member with id: {id}"
        )
        try:
            data = request.get_json()
            crew_member_schema.validate(data)
            updated_crew = crew_member_schema.load(data, instance=cm, partial=True)
            db.session.commit()
            return crew_member_schema.dump(updated_crew), 200
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))

    @jwt_required()
    def delete(self, id):
        cm = CrewMember.query.get_or_404(
            id, description=f"Could not find crew_member with id: {id}"
        )
        try:
            db.session.delete(cm)
            db.session.commit()
            return None, 204
        except Exception as e:
            db.session.rollback()
            abort(400, str(e))
