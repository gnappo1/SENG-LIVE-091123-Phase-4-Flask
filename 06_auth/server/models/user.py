from . import validates, re
from app_setup import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        self._password_hash = hashed_password
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
