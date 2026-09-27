
from faker import Faker

fake = Faker()

def generate_courier_data():
    return {
        "login": fake.user_name(),
        "password": fake.password(),
        "firstName": fake.first_name()
    }

