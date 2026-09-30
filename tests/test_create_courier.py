import requests
from data import Url
from constants import EXPECTED_STATUS_CREATED, EXPECTED_STATUS_CONFLICT, EXPECTED_STATUS_BAD_REQUEST, MSG_LOGIN_DUPLICATE, MSG_ENOUGH_DATA_CREATE_ACCOUNT

from generators import generate_courier_data
import allure

class TestCreateCourier:

    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self):
        courier_data = generate_courier_data()
        
        response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier_data)

        assert EXPECTED_STATUS_CREATED == response.status_code, (
            f'Ожидаемый статус-код: 201. '
            f'Фактический статус-код: {response.status_code}. '
        )
        assert response.json() == {"ok": True}, (
            f'Ожидаемый результат: в теле ответа присутствует поле "ok" со значением "True". '
            f'Фактический результат: тело ответа {response.text}. '
        )

    @allure.title('Создание двух одинаковых курьеров')
    def test_create_duplicate_courier(self, courier):
                
        requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier)
        second_response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier)
        actual_message = second_response.json()["message"]
        
        assert EXPECTED_STATUS_CONFLICT == second_response.status_code, (
            f'Ожидаемый статус-код: 409. '
            f'Фактический статус-код: {second_response.status_code}. '
        )
        assert MSG_LOGIN_DUPLICATE in actual_message, (
            f'Ожидаемое сообщение в теле ответа содержит фразу MSG_LOGIN_DUPLICATE. '
            f'Фактическое сообщение в теле ответа: {actual_message}. '
        )

    @allure.title('Создание курьера без обязательного поля Логин')
    def test_withowt_login(self):
        courier_data = generate_courier_data()
        courier_data.pop('login')

        response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier_data)
        actual_message = response.json()["message"]

        assert response.status_code == EXPECTED_STATUS_BAD_REQUEST, (
            f'Ожидаемый статус-код: 400. '
            f'Фактический статус-код: {response.status_code}. '
        )
        assert MSG_ENOUGH_DATA_CREATE_ACCOUNT in actual_message, (
            f'Ожидаемое сообщение в теле ответа содержит фразу MSG_ENOUGH_DATA_CREATE_ACCOUNT. '
            f'Фактическое сообщение в теле ответа: {actual_message}. '
        )

    @allure.title('Создание курьера без обязательного поля Пароль')
    def test_withowt_password(self):
        courier_data = generate_courier_data()
        courier_data.pop('password')

        response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier_data)
        actual_message = response.json()["message"]

        assert response.status_code == EXPECTED_STATUS_BAD_REQUEST, (
            f'Ожидаемый статус-код: 400. '
            f'Фактический статус-код: {response.status_code}. '
        )
        assert MSG_ENOUGH_DATA_CREATE_ACCOUNT in actual_message, (
            f'Ожидаемое сообщение в теле ответа содержит фразу MSG_ENOUGH_DATA_CREATE_ACCOUNT. '
            f'Фактическое сообщение в теле ответа: {actual_message}. '
        )


    @allure.title('Создание курьера с уже существующим логином')
    def test_create_duplicate_login(self, courier):
    
        duplicate_courier = {'login': courier['login'], 'password': 'nvjfjmdh7659', 'firstName': 'Kapulka'}
        response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=duplicate_courier)
        actual_message = response.json()["message"]

        assert EXPECTED_STATUS_CONFLICT == response.status_code, (
            f'Ожидаемый статус-код: 409. '
            f'Фактический статус-код: {response.status_code}. '
        )
        assert MSG_LOGIN_DUPLICATE in actual_message, (
            f'Ожидаемое сообщение в теле ответа содержит фразу MSG_LOGIN_DUPLICATE. '
            f'Фактическое сообщение в теле ответа: {actual_message}. '
        )

        

    




