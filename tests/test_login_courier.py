import requests
from data import Url
from constants import EXPECTED_STATUS_SUCCESS, EXPECTED_STATUS_GATEWAY_TIMEOUT, EXPECTED_STATUS_BAD_REQUEST, EXPECTED_STATUS_NOT_FOUND, MSG_NOT_FOUND_ACCOUNT, LITTLE_DATA_FOR_LOGIN, MSG_SERVICE_UNAVAIBLE
import allure

class TestLoginCourier:

    @allure.title('Успешная авторизация курьера')
    def test_login_success(self, courier):

        login = courier['data']['login']
        password = courier['data']['password']
        
        response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'login': login, 'password': password})
        
        assert EXPECTED_STATUS_SUCCESS == response.status_code, (
            f'Ожидаемый статус-код: 200. '
            f'Фактический статус-код: {response.status_code}. '
        )

        assert 'id' in response.json(), (
            f'Ожидаемый результат: в теле ответа присутствует поле "id". '
            f'Фактический результат: тело ответа {response.text}. '
        )


    @allure.title('Авторизация курьера без обязательного поля Пароль')
    @allure.description('Ожидаем 504 вместо 400, так как в сервисе есть известный баг: ' \
    'при отсутствии пароля сервис не успевает обработать валидацию и падает по таймауту.' \
    'assert response.status_code == 504')
    
    def test_login_without_password(self, courier):

        login = courier['data']['login']

        response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'login': login})

        assert EXPECTED_STATUS_GATEWAY_TIMEOUT == response.status_code, (
            f'Ожидаемый статус-код: 504. '
            f'Фактический статус-код: {response.status_code}. '
        )

        assert MSG_SERVICE_UNAVAIBLE in response.text.lower(), (
            f'Ожидаемое сообщение в теле ответа содержит фразу MSG_SERVICE_UNAVAIBLE. '
            f'Фактическое сообщение в теле ответа: "{response.text}"'
        ) 



    @allure.title('Авторизация курьера без обязательного поля Логин')
    def test_login_without_login(self, courier):

        password = courier['data']['password']

        response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'password': password})
        actual_message = response.json()["message"]

        assert EXPECTED_STATUS_BAD_REQUEST == response.status_code, (
            f'Ожидаемый статус-код: 400. '
            f'Фактический статус-код: {response.status_code}. '
        )

        assert LITTLE_DATA_FOR_LOGIN in actual_message, (
            f'Ожидаемое сообщение в теле ответа содержит фразу LITTLE_DATA_FOR_LOGIN. '
            f'Фактическое сообщение в теле ответа: {actual_message}. '
        )


    @allure.title('Авторизация курьера с неправильным паролем')
    def test_login_incorrect_password(self, courier):

        login = courier['data']['login']

        response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'login': login, 'password': ['12345']})
        actual_message = response.json()["message"]
        
        assert EXPECTED_STATUS_NOT_FOUND == response.status_code, (
            f'Ожидаемый статус-код: 404. '
            f'Фактический статус-код: {response.status_code}. '
            f'Тело ответа: {response.text}'
        )

        assert MSG_NOT_FOUND_ACCOUNT in actual_message, (
            f'Ожидаемое сообщение в теле ответа содержит фразу MSG_NOT_FOUND_ACCOUNT. '
            f'Фактическое сообщение в теле ответа: {actual_message}. '
        )


    @allure.title('Авторизация курьера с неправильным логином')
    def test_login_incorrect_login(self, courier):

        password = courier['data']['password']

        response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'login': ['nvnjnv'], 'password': password})
        actual_message = response.json()["message"]
            
        assert EXPECTED_STATUS_NOT_FOUND == response.status_code, (
            f'Ожидаемый статус-код: 404. '
            f'Фактический статус-код: {response.status_code}. '
            f'Тело ответа: {response.text}'
        )
        
        assert MSG_NOT_FOUND_ACCOUNT in actual_message, (
            f'Ожидаемое сообщение в теле ответа содержит фразу MSG_NOT_FOUND_ACCOUNT. '
            f'Фактическое сообщение в теле ответа: {actual_message}. '
        )


    @allure.title('Авторизация курьера под несуществующим пользователем')
    def test_login_user_not_exist(self):
            response = requests.post(f'{Url.MAIN_URL}{Url.LOGIN_COURIER}', json={'login': 'fhfmk', 'password': '12345'})
            actual_message = response.json()["message"]
            
            assert EXPECTED_STATUS_NOT_FOUND == response.status_code, (
            f'Ожидаемый статус-код: 404. '
            f'Фактический статус-код: {response.status_code}. '
            f'Тело ответа: {response.text}'
        )
            assert MSG_NOT_FOUND_ACCOUNT in actual_message, (
            f'Ожидаемое сообщение в теле ответа содержит фразу MSG_NOT_FOUND_ACCOUNT. '
            f'Фактическое сообщение в теле ответа: {actual_message}. '
        )
                


    