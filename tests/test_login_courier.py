import requests
from data import Url
import allure

class TestLoginCourier:

    @allure.title('Успешная авторизация курьера')
    def test_login_success(self, courier):
        response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'login': courier['login'], 'password': courier['password']})
        
        assert 200 == response.status_code, (
            f'Ожидаемый статус-код: 200. '
            f'Фактический статус-код: {response.status_code}. '
        )

        assert 'id' in response.json(), (
            f'Ожидаемый результат: в теле ответа присутствует поле "id". '
            f'Фактический результат: тело ответа {response.text}. '
        )


    @allure.title('Авторизация курьера без обязательного поля Пароль')
    def test_login_without_password(self, courier):
        response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'login': courier['login']})
        
        assert 400 == response.status_code, (
            f'Ожидаемый статус-код: 400. '
            f'Фактический статус-код: {response.status_code}. '
            f'Тело ответа: {response.text}'
        )
        assert response.json() == {"message": "Недостаточно данных для входа"}, (
            f'Ожидаемое сообщение в теле ответа: "Недостаточно данных для входа". '
            f'Фактическое сообщение в теле ответа: {response.json()}. '
        )


    @allure.title('Авторизация курьера с неправильным паролем')
    def test_login_incorrect_password(self, courier):
        response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'login': courier['login'], 'password': ['12345']})
        
        assert 404 == response.status_code, (
            f'Ожидаемый статус-код: 404. '
            f'Фактический статус-код: {response.status_code}. '
            f'Тело ответа: {response.text}'
        )

        assert response.json() == {"message": "Учетная запись не найдена"}, (
            f'Ожидаемое сообщение в теле ответа: "Учетная запись не найдена". '
            f'Фактическое сообщение в теле ответа: {response.json()}. '
        )


    @allure.title('Авторизация курьера под несуществующим пользователем')
    def test_login_user_not_exist(self):
            response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'login': 'fhfmk', 'password': '12345'})
            
            assert 404 == response.status_code, (
            f'Ожидаемый статус-код: 404. '
            f'Фактический статус-код: {response.status_code}. '
            f'Тело ответа: {response.text}'
        )
            assert response.json() == {"message": "Учетная запись не найдена"}, (
            f'Ожидаемое сообщение в теле ответа: "Учетная запись не найдена". '
            f'Фактическое сообщение в теле ответа: {response.json()}. '
        )
                


    