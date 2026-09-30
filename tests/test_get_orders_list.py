import requests
import pytest
from data import Url
from constants import EXPECTED_STATUS_SUCCESS
import allure


class TestGetOrdersList:

    @allure.title('Тело ответа списка заказов')
    @allure.description('Проверка, что в теле ответа возвращается список заказов')

    def test_get_orders_list(self):

        response = requests.get(f'{Url.MAIN_URL}{Url.CREATE_ORDER}')

        assert EXPECTED_STATUS_SUCCESS == response.status_code, (
            f'Ожидаемый статус-код: 200. '
            f'Фактический статус-код: {response.status_code}. '
        )

        assert isinstance(response.json()["orders"], list), (
            f'Ожидаемый тип данных: list. '
            f'Фактический тип данных: {type(response.json()["orders"]).__name__}. '
        )