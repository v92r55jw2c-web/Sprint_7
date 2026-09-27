import requests
import pytest
from data import Url
import allure

class TestCreateOrder:
    @pytest.mark.parametrize(
        'color',
        [
            ['BLACK'],
            ['GREY'],
            ['BLACK', 'GREY']
        ]
    )
    @allure.title('Создание заказа с указанием цвета/цветов')
    def test_create_order_with_color(self, color):

        order_data = {
            "firstName": "Оля",
            "lastName": "Михеева",
            "address": "Москва, улица Ленина, 1",
            "metroStation": "Нахимовский проспект",
            "phone": "+79991245867",
            "rentTime": 2,
            "deliveryDate": "2026-09-27",
            "comment": "Позвонить перед доставкой",
            "color": color
        }

        response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_ORDER}', json=order_data)
        
        assert 201 == response.status_code, (
            f'Ожидаемый статус-код: 201. '
            f'Фактический статус-код: {response.status_code}. '
        )
        assert 'track' in response.json(), (
            f'Ожидаемый результат: в теле ответа присутствует поле "track". '
            f'Фактический результат: тело ответа {response.text}. '
        )


    @allure.title('Создание заказа без указания цвета')
    def test_create_order_without_color(self):

        order_data = {
            "firstName": "Оля",
            "lastName": "Михеева",
            "address": "Москва, улица Ленина, 1",
            "metroStation": "Нахимовский проспект",
            "phone": "+79991245867",
            "rentTime": 2,
            "deliveryDate": "2026-09-27",
            "comment": "Позвонить перед доставкой"
        }

        response = requests.post(f'{Url.MAIN_URL}{Url.CREATE_ORDER}', json=order_data)
                
        assert 201 == response.status_code, (
            f'Ожидаемый статус-код: 201. '
            f'Фактический статус-код: {response.status_code}. '
        )
        assert 'track' in response.json(), (
            f'Ожидаемый результат: в теле ответа присутствует поле "track". '
            f'Фактический результат: тело ответа {response.text}. '
        )