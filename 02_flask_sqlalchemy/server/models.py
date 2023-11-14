from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Production(db.Model):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String, nullable=False)
    director = db.Column(db.String)
    description = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    crew_members = db.relationship(
        "CrewMember", back_populates="production", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"""
            <Production #{self.id}:
                Title: {self.title}
                Genre: {self.genre}
                Director: {self.director}
                Description: {self.description}
                Budget: {self.budget}
                Image: {self.image}
                Ongoing: {self.ongoing}
            />
        """

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "director": self.director,
            "budget": self.budget,
            "image": self.image,
            "ongoing": self.ongoing,
            "description": self.description,
        }


class CrewMember(db.Model):
    __tablename__ = "crew_members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    production = db.relationship("Production", back_populates="crew_members")

    def __repr__(self):
        return f"""
            <Crewmember #{self.id}:
                Name: {self.name}
                Role: {self.role}
                Production Id: {self.production_id}
            />
        """

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "production_id": self.production_id,
        }
