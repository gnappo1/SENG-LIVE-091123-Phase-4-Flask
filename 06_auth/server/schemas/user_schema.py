from . import fields, validate
from models.user import User
from app_setup import ma


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    email = fields.Email(required=True)
    password_hash = fields.String(validate=validate.Length(min=10, max=50))

    #! Create hyperlinks for easy navigation of your api
    # url = ma.Hyperlinks(
    #     {
    #         "self": ma.URLFor("userbyid", values=dict(id="<id>")),
    #         "collection": ma.URLFor("users"),
    #     }
    # )
