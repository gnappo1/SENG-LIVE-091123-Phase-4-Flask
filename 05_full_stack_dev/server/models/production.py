from . import validates, re
from app_setup import db
class Production(db.Model):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=False)
    ongoing = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    # &* Relationships
    crew_members = db.relationship(
        "CrewMember", back_populates="production", cascade="all"
    )

    def __repr__(self):
        return (
            f"<Production #{self.id}:\n"
            + f"Title: {self.title}"
            + f"Genre: {self.genre}"
            + f"Director: {self.director}"
            + f"Budget: {self.budget}"
            + f"Image: {self.image}"
            + f"Ongoing: {self.ongoing}"
            + f"Description: {self.description}"
        )

    @validates("title")
    def validate_title(self, _, title):
        if not isinstance(title, str):
            raise TypeError("Titles must be strings")
        elif len(title) < 3:
            raise ValueError(f"{title} has to be at least 3 characters long")
        return title

    @validates("genre")  # presence and inclusion
    def validate_genre(self, _, genre):
        if not isinstance(genre, str):
            raise TypeError("Genres must be strings")
        elif genre not in ["Drama", "Musical", "Opera"]:
            raise ValueError(f"{genre} has to be one of Drama, Musical, Opera")
        return genre

    @validates("director")
    def validate_director(self, _, director):
        if not isinstance(director, str):
            raise TypeError("Directors must be strings")
        elif len(director.split(" ")) < 2:
            raise ValueError(f"{director} has to be a string of at least two words")
        return director

    @validates("description")
    def validate_description(self, _, description):
        if not isinstance(description, str):
            raise TypeError("Descriptions must be strings")
        elif len(description) < 10:
            raise ValueError(
                f"{description} has to be a string of at least 10 characters"
            )
        return description

    @validates("budget")
    def validate_budget(self, _, budget):
        if not isinstance(budget, float):
            raise TypeError("Budgets must be floats")
        elif budget < 0 or budget > 10000000:
            raise ValueError(f"{budget} has to be a positive float under 10Millions")
        return budget

    @validates("image")
    def validate_image(self, _, image):
        if not isinstance(image, str):
            raise TypeError("Images must be strings")
        elif not re.match(r"^https?:\/\/.*\.(?:png|jpeg|jpg)$", image):
            raise ValueError(
                f"{image} has to be a string of a valid url ending in png, jpeg or jpg"
            )
        return image

    @validates("ongoing")
    def validate_ongoing(self, _, ongoing):
        if not isinstance(ongoing, bool):
            raise ValueError(f"Ongoing has to be a boolean")
        return ongoing
