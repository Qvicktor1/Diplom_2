import pytest
import requests
import allure
from datetime import datetime

from data import Urls


class TestGetUserOrders:

    @allure.title('Test of getting user orders with authorization')
    @allure.description('Test of the endpoint "Получение заказов конкретного пользователя" GET /api/orders.'
                        'Checks that response code is 200 '
                        'that response body contains all required fields'
                        'and that request returns "success": true')
    def test_get_user_orders_with_authorization(self, create_user):
        payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
        headers = {'Authorization': f'{create_user[2]}'}
        requests.post(Urls.create_order_url, data=payload, headers=headers)
        response = requests.get(Urls.get_user_orders, headers=headers)
        assert response.status_code == 200, f'Instead of code 200 received code {response.status_code}'
        assert response.json().get('success') is True, 'Field "success" is not True in the response body'
        assert 'orders' in response.json(), 'Field "orders" is missing in the response body'
        assert 'total' in response.json(), 'Field "orders" is missing in the response body'
        assert 'totalToday' in response.json(), 'Field "orders" is missing in the response body'
        orders_data = response.json().get('orders')[0]
        assert '_id' in orders_data, 'Field "_id" is missing in the "orders" field of the response body'
        assert 'ingredients' in orders_data, 'Field "ingredients" is missing in the "orders" field of the response body'
        assert 'status' in orders_data, 'Field "status" is missing in the "orders" field of the response body'
        assert 'createdAt' in orders_data, 'Field "createdAt" is missing in the "orders" field of the response body'
        assert 'updatedAt' in orders_data, 'Field "updatedAt" is missing in the "orders" field of the response body'
        assert 'number' in orders_data, 'Field "number" is missing in the "orders" field of the response body'

    @allure.title('Test of sorting user orders with authorization')
    @allure.description('Test of the endpoint "Получение заказов конкретного пользователя" GET /api/orders.'
                        'Checks that response contains user orders sorted by Update time ascending'
                        'that response code is 200 '
                        'and that request returns "success": true')
    def test_sorting_user_orders_with_authorization(self, create_user, create_n_orders):
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.get(Urls.get_user_orders, headers=headers)
        assert response.status_code == 200, f'Instead of code 200 received code {response.status_code}'
        assert response.json().get('success') is True, 'Field "success" is not True in the response body'
        orders = response.json().get('orders')
        sorted_orders = sorted(orders, key=lambda x: datetime.strptime(x['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                               reverse=False)
        assert orders == sorted_orders, 'User orders are not sorted by update time in descending order'

    @allure.title('Test of failed attempt to get user orders without authorization')
    @allure.description('Negative test of the endpoint "Получение заказов конкретного пользователя" GET /api/orders.'
                        'Checks that response code is 401 '
                        'that response body contains all required fields'
                        'and that request returns "success": false')
    def test_get_user_orders_without_authorization_failed(self, create_user):
        payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
        headers = {'Authorization': f'{create_user[2]}'}
        requests.post(Urls.create_order_url, data=payload, headers=headers)
        headers = {}
        response = requests.get(Urls.get_user_orders, headers=headers)
        assert response.status_code == 401, f'Instead of code 401 received code {response.status_code}'
        assert response.json().get('success') is False, 'Field "success" is not False in the response body'
        assert response.json()['message'] == 'You should be authorised', f'Error message contains wrong text'