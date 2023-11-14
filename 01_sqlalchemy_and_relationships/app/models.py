from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    String,
    DateTime,
    PrimaryKeyConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Table,
    CheckConstraint,
    func,
)

import re
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

Base = declarative_base(metadata=metadata)

owner_pet_association = Table(
    "owner_pets",
    Base.metadata,
    # Column("id", Integer, primary_key=True),
    Column("owner_id", Integer, ForeignKey("owners.id"), primary_key=True),
    Column("pet_id", Integer, ForeignKey("pets.id"), primary_key=True),
)


# class PetOwner(Base):
#     __tablename__ = "pet_owners"
#     id = Column(Integer, primary_key=True)
#     pet_id = Column(Integer, ForeignKey("pets.id"))
#     owner_id = Column(Integer, ForeignKey("owners.id"))
#     pet = relationship("Pet", back_populates="pet_owners")
#     owner = relationship("Owner", back_populates="pet_owners")

#     def __repr__(self):
#         return (
#             f"<PetOwner #{self.id} \n"
#             + f"pet id: {self.pet_id}\n"
#             + f"owner id: {self.owner_id}\n"
#         )


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(Integer, unique=True)
    address = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    #! one-to-many
    # pets = relationship("Pet", backref=backref("owner"))
    #! many-to-many w Model
    # pet_owners = relationship("PetOwner", back_populates="owner")
    # pets = association_proxy("pet_owners", "pet")
    #! many-to-many w Table
    pets = relationship("Pet", secondary=owner_pet_association, back_populates="owners")

    def __repr__(self):
        return (
            f"<Owner #{self.id} \n"
            + f"name: {self.name}\n"
            + f"email: {self.email}\n"
            + f"phone: {self.phone}\n"
            + f"address: {self.address}\n"
        )


class Pet(Base):
    __tablename__ = "pets"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="owner_pk"),
        CheckConstraint("length(name) > 0", name="owner_name_length"),
    )

    id = Column(Integer)
    name = Column(String, nullable=False)
    species = Column(String)
    breed = Column(String)
    temperament = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    #! many-to-many w Model
    # pet_owners = relationship("PetOwner", back_populates="pet")
    # owners = association_proxy("pet_owners", "owner")
    #! many-to-many with Table
    owners = relationship(
        "Owner", secondary=owner_pet_association, back_populates="pets"
    )

    def __repr__(self):
        return (
            f"<Pet #{self.id} \n"
            + f"name: {self.name}\n"
            + f"species: {self.species}\n"
            + f"breed: {self.breed}\n"
            + f"temperament: {self.temperament}\n"
        )
