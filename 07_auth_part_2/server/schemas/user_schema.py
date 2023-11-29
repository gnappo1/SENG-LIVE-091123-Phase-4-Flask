from . import fields, validate
from models.user import User
from app_setup import ma

class UserSchema(ma.SQLAlchemySchema):
    class Meta():
        model = User
        load_instance = True
        
    id = fields.Integer()
    email = fields.Email(required=True)
    username = fields.String(required=True)
    password_hash = fields.String(validate=validate.Length(min=10, max=50))
