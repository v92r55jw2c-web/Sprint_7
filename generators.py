import random
from faker import Faker

fake = Faker()

def generate_courier_data():

    base_login = fake.user_name()
    unique_suffix = random.randint(1000, 9999)
    login = f"{base_login}{unique_suffix}"

    return {
        "login": login,
        "password": fake.password(),
        "firstName": fake.first_name()
    }

