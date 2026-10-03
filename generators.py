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

def generate_order_data(color=None):
    
    data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": f"Москва, ул. Тестовая, д. {fake.random_int(min=1, max=100)}",
        "metroStation": "Нахимовский проспект",
        "phone": f"+7999{fake.random_number(digits=7)}",
        "rentTime": 2,
        "deliveryDate": "2026-09-27",
        "comment": "Оставить у подъезда"
    }
    
    if color is not None:
        data["color"] = color
        
    return data  