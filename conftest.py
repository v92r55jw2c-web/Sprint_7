import pytest
import requests
from data import Url
from generators import generate_courier_data, generate_order_data
from faker import Faker

# Фикстура создания курьера
@pytest.fixture
def courier():
    courier_data = generate_courier_data()
    response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier_data)

    courier_id = response.json().get('id') or courier_data['login']

    yield {
        "data": courier_data,
        "response": response,
        "id": courier_id
    }

    requests.delete(f'{Url.MAIN_URL}{Url.CREATE_COURIER}/{courier_id}')


#Фикстура создания заказа с указанием цвета
@pytest.fixture(params=[
    ['BLACK'],
    ['GREY'],
    ['BLACK', 'GREY']])

def order_with_color(request):
    color = request.param

    order_data = generate_order_data(color=color)

    response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_ORDER}', json=order_data)
    track_id = response.json().get('track')
    
    yield {
        "track_id": track_id,
        "expected_color": color,
        "response": response
    }

    requests.put(f'{Url.MAIN_URL}{Url.CANCEL_ORDER}', params={"track": track_id})


#Фикстура создания заказа без указания цвета
@pytest.fixture
def order_without_color():

    order_data = generate_order_data(color=None)

    response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_ORDER}', json=order_data)
    track_id = response.json().get('track')
        
    yield {
        "track_id": track_id,
        "response": response
    }

    requests.put(f'{Url.MAIN_URL}{Url.CANCEL_ORDER}', params={"track": track_id})