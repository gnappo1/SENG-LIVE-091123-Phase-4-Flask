from . import validates, re
from .production import Production
from app_setup import db


class CrewMember(db.Model):
    __tablename__ = "crew_members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production = db.relationship("Production", back_populates="crew_members")

    def __repr__(self):
        return (
            f"<CrewMember #{self.id}:\n"
            + f"Name: {self.name}"
            + f"Role: {self.role}"
            + f"Production_id: {self.production_id}"
        )

    @validates("name")
    def validate_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Names must be strings")
        elif len(name.split(" ")) < 2:
            raise ValueError(f"{name} has to be at least 2 words")
        return name

    @validates("role")
    def validate_role(self, _, role):
        if not isinstance(role, str):
            raise TypeError("Roles must be strings")
        elif len(role) < 2:
            raise ValueError(f"{role} has to be at least 3 characters long")
        return role

    @validates("production_id")
    def validate_production_id(self, _, production_id):
        if not isinstance(production_id, int):
            raise TypeError("Production ids must be integers")
        elif production_id < 1:
            raise ValueError(f"{production_id} has to be a positive integer")
        elif not db.session.get(Production, production_id):
            raise ValueError(
                f"{production_id} has to correspond to an existing production"
            )
        return production_id
