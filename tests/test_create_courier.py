import requests
from data import Url
from generators import generate_courier_data
import allure

class TestCreateCourier:

    @allure.title('Успешное создание курьера')
    def test_create_courier_success(self):
        courier_data = generate_courier_data()
        
        response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier_data)

        assert 201 == response.status_code, (
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
        
        assert 409 == second_response.status_code, (
            f'Ожидаемый статус-код: 409. '
            f'Фактический статус-код: {second_response.status_code}. '
        )
        assert second_response.json() == {"message": "Этот логин уже используется"}, (
            f'Ожидаемое сообщение в теле ответа: "Этот логин уже используется". '
            f'Фактическое сообщение в теле ответа: {second_response.json()}. '
        )

    @allure.title('Создание курьера без обязательного поля Логин')
    def test_withowt_login(self):
        courier_data = generate_courier_data()
        courier_data.pop('login')

        response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=courier_data)

        assert response.status_code == 400, (
            f'Ожидаемый статус-код: 400. '
            f'Фактический статус-код: {response.status_code}. '
        )
        assert response.json() == {"message": "Недостаточно данных для создания учетной записи"}, (
            f'Ожидаемое сообщение в теле ответа: "Недостаточно данных для создания учетной записи". '
            f'Фактическое сообщение в теле ответа: {response.json()}. '
        )
        
    @allure.title('Создание курьера с уже существующим логином')
    def test_create_duplicate_login(self, courier):
    
        duplicate_courier = {'login': courier['login'], 'password': 'nvjfjmdh7659', 'firstName': 'Kapulka'}
        response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=duplicate_courier)

        assert 409 == response.status_code, (
            f'Ожидаемый статус-код: 409. '
            f'Фактический статус-код: {response.status_code}. '
        )
        assert response.json() == {"message": "Этот логин уже используется"}, (
            f'Ожидаемое сообщение в теле ответа: "Этот логин уже используется". '
            f'Фактическое сообщение в теле ответа: {response.json()}. '
        )

        

    




