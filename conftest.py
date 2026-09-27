import pytest
import requests
from data import Url
from generators import generate_courier_data


@pytest.fixture
def courier():
    courier_data = generate_courier_data()
    requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier_data)

    login_response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={
            'login': courier_data['login'],
            'password': courier_data['password']})

    assert login_response.status_code == 200, (
    f'LOGIN: {login_response.status_code} {login_response.text}')
    
    courier_id = login_response.json()['id']

    yield courier_data

    delete_response = requests.delete(
    f'{Url.MAIN_URL}{Url.CREATE_COURIER}/{courier_id}')

    assert delete_response.status_code == 200
    assert delete_response.json() == {"ok": True}   