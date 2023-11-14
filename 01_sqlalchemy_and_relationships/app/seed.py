from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Pet, Owner
# from datetime import date, timedelta

if __name__ == '__main__':
    engine = create_engine('sqlite:///pet_app.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    # with Session.begin() as session:

    # 2.a ✅ Add delete methods for Pet and Owner to clear the database before each seeding
    session.query(Pet).delete()
    session.query(Owner).delete()

    # Initialize faker
    fake = Faker()

    # Create List of species with "Cat" and "Dog"
    species = ["Cat", "Dog"]

    # Create a List of cat breeds
    cat_breeds = ["Domestic Long Hair", "Domestic Short Hair", "Siamese", "Ragdoll", "Sphynx", "Burmese"]

    # Create a List of dog breeds
    dog_breeds = ["Mix", "Husky", "Malamute", "Dachshound", "Samoyed", "Shiba Inu", "Corgi" ]

    # Create a List of temperaments 
    temperaments = ["Calm", "Nervous", "Mischievous", "Aggressive", "Hyper" ]

    # Create an empty List of owners
    owners = []

    # Create a for loop that iterates 50 times
    for _ in range(50):
            
            # Create an owner using data from faker
        owner = Owner(
            name=f"{fake.first_name()} {fake.last_name()}",
            email=fake.email(),
            phone=random.randint(1000000000, 9999999999),
            address=fake.address()
        )
        
        # Use .add and .commit to save the owner one at a time, so we maintain the owner ID in our instance.
        session.add(owner)
        session.commit()
        
        # Append each new owner to the owners array
        owners.append(owner)
    
    # Create an empty pets array
    pets = []
    # Create a for loop that iterates over the owners array
    # for owner in owners:

        # Create a for loop that iterates 1 - 3 times
    for _ in range (100):

        # Use faker and the species, cat breeds, dog breeds and temperament Lists to create a pet
        rand_species = random.choice(species)

        pet = Pet(
            name=fake.name(),
            species=rand_species,
            breed=random.choice(cat_breeds) if rand_species == "Cat" else random.choice(dog_breeds),
            temperament=random.choice(temperaments),
            # owner_id=owner.id
        )

        # Use .add and .commit to save the pet to the database
        session.add(pet)
        session.commit()
    
        # Append the pet to the pets array
        pets.append(pet)
    import ipdb; ipdb.set_trace()