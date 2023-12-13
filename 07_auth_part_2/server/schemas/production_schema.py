from . import fields, validate
from models.production import Production
from .crew_member_schema import CrewMemberSchema
from app_setup import ma


class ProductionSchema(ma.SQLAlchemySchema):
    class Meta():
        model = Production
        load_instance = True
        

    crew_members = fields.Nested(
        CrewMemberSchema,
        only=("id", "name", "role"),
        exclude=("production",),
        many=True,
        dump_only=True
    )
    id = fields.Integer()
    title = fields.String(required=True, validate=validate.Length(min=2, max=50))
    director = fields.String(required=True, validate=validate.Length(min=2, max=50))
    ongoing = fields.Boolean()
    description = fields.String(
        required=True, validate=validate.Length(min=30, max=500)
    )
    genre = fields.String(required=True, validate=validate.Length(min=2, max=50))
    image = fields.String(
        required=True,
        validate=validate.Regexp(
            r".*\.(jpeg|png|jpg)", error="File URI must be in JPEG or PNG format"
        ),
    )
    budget = fields.Float(
        required=True, validate=validate.Range(min=0.99, max=500000000)
    )

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor("productionbyid", values=dict(id="<id>")),
            "collection": ma.URLFor("productions"),
            "crewmembers": ma.URLFor("crewmembers"),
        }
    )
