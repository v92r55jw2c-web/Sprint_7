import requests
import pytest
from data import Url
from constants import EXPECTED_STATUS_CREATED
import allure

class TestCreateOrder:

    @allure.title('Создание заказа с указанием цвета/цветов')
    def test_create_order_with_color(self, order_with_color):

        track_id = order_with_color["track_id"]
        response = order_with_color["response"]
        
        assert EXPECTED_STATUS_CREATED == response.status_code, (
            f'Ожидаемый статус-код: 201. '
            f'Фактический статус-код: {response.status_code}. '
        )

        assert track_id is not None

        assert 'track' in response.json(), (
            f'Ожидаемый результат: в теле ответа присутствует поле "track". '
            f'Фактический результат: тело ответа {response.text}. '
        )


    @allure.title('Создание заказа без указания цвета')
    def test_create_order_without_color(self, order_without_color):

        track_id = order_without_color["track_id"]
        response = order_without_color["response"]
                
        assert EXPECTED_STATUS_CREATED == response.status_code, (
            f'Ожидаемый статус-код: 201. '
            f'Фактический статус-код: {response.status_code}. '
        )

        assert track_id is not None

        assert 'track' in response.json(), (
            f'Ожидаемый результат: в теле ответа присутствует поле "track". '
            f'Фактический результат: тело ответа {response.text}. '
        )