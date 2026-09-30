import pytest
import requests
from data import Url
from generators import generate_courier_data
from faker import Faker

# Фикстура создания курьера
@pytest.fixture
def courier():
    courier_data = generate_courier_data()
    requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier_data)

    login_response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={
            'login': courier_data['login'],
            'password': courier_data['password']})
    
    try:
        courier_id = login_response.json()['id']
    except (KeyError, TypeError):
        courier_id = None

    
    yield courier_data

    if courier_id:
        try:
             requests.delete(f'{Url.MAIN_URL}{Url.CREATE_COURIER}/{courier_id}')
        except Exception:
            pass



#Фикстура создания заказа с указанием цвета
fake = Faker('ru_RU')

@pytest.fixture(params=[
    ['BLACK'],
    ['GREY'],
    ['BLACK', 'GREY']])

def order_with_color(request):
    color = request.param

    order_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": f"Москва, ул. Тестовая, д. {fake.random_int(min=1, max=100)}",
        "metroStation": "Нахимовский проспект",
        "phone": f"+7999{fake.random_number(digits=7)}",
        "rentTime": 2,
        "deliveryDate": "2026-09-27",
        "comment": "Оставить у подьезда",
        "color": color
    }

    response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_ORDER}', json=order_data)
    track_id = response.json().get('track')

    yield {
        "track_id": track_id,
        "expected_color": color,
        "response": response
    }

    try:
        cancel_response = requests.put(f'{Url.MAIN_URL}{Url.CANCEL_ORDER}', json={"track": track_id})
        print(f"[Cleanup] Заказ {track_id} отменен. Статус отмены: {cancel_response.status_code}")

    except Exception as e:
        print(f"[Cleanup Error] Не удалось отменить заказ {track_id}: {e}")


    #Фикстура создания заказа без указания цвета
@pytest.fixture
def order_without_color():
    order_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": f"Москва, ул. Тестовая, д. {fake.random_int(min=1, max=100)}",
        "metroStation": "Нахимовский проспект",
        "phone": f"+7999{fake.random_number(digits=7)}",
        "rentTime": 2,
        "deliveryDate": "2026-09-27",
        "comment": "Без цвета" 
    }

    response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_ORDER}', json=order_data)
    track_id = response.json().get('track')
        
    yield {
        "track_id": track_id,
        "response": response
    }

    try:
        cancel_resp = requests.put(f'{Url.MAIN_URL}/api/v1/orders/cancel', json={"track": track_id})
        print(f"[Cleanup] Заказ {track_id} отменен. Статус отмены: {cancel_resp.status_code}")
    
    except Exception as e:
        print(f"[Cleanup Error] Не удалось отменить заказ {track_id}: {e}") 