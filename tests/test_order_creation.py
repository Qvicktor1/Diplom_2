import requests
import allure

from data import Urls


class TestOrderCreation:

    @allure.title('Test of successful order creation with authorization and ingredients')
    @allure.description('Test of the endpoint "Создание заказа" POST /api/orders.'
                        'Checks the creation of the order with authorization and ingredients '
                        'that response body contains all main required fields,'
                        'and that a successful request returns "success": true')
    def test_order_creation_with_authorization_and_ingredients(self, create_user):
        payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.post(Urls.create_order_url, data=payload, headers=headers)
        assert response.status_code == 200, f'Failed to create order, code {response.status_code}'
        assert response.json().get('success') is True, 'Field "success" is not True in the response body'
        assert 'name' in response.json(), 'Field "name" is missing in the response body'
        assert 'order' in response.json(), 'Field "order" is missing in the response body'
        order_data = response.json().get('order')
        assert 'number' in order_data, 'Field "number" is missing in the "order" field of the response body'

    @allure.title('Test of failed attempt to create an order without authorization')
    @allure.description('Test of the endpoint "Создание заказа" POST /api/orders.'
                        'Checks that order creation is impossible without authorization '
                        'that response body contains all main required fields,'
                        'and that request returns "success": False')
    def test_order_creation_without_authorization_failed(self):
        payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
        response = requests.post(Urls.create_order_url, data=payload)
        """Согласно документации, раздел "Авторизация и регистрация", стр 5 - "Только авторизованные пользователи могут делать заказы".
        {"success": false, "message": "You should be authorised"}"""
        assert response.status_code == 401, f'Instead of code 401 received code {response.status_code}'
        assert response.json().get('success') is False, 'Field "success" is not True in the response body'
        assert response.json()['message'] == 'You should be authorised', f'Error message contains wrong text'

    @allure.title('Test of failed attempt to create an order without ingredients')
    @allure.description('Negative test of the endpoint "Создание заказа" POST /api/orders.'
                        'Checks the creation of the order without ingredients '
                        'that response body contains all required fields'
                        'and that request returns "success": false')
    def test_order_creation_without_ingredients_failed(self, create_user):
        payload = {}
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.post(Urls.create_order_url, data=payload, headers=headers)
        assert response.status_code == 400, f'Instead of code 400 received code {response.status_code}'
        assert response.json().get('success') is False, 'Field "success" is not False in the response body'
        assert response.json()['message'] == 'Ingredient ids must be provided', f'Error message contains wrong text'

    @allure.title('Test of failed attempt to create an order with wrong ingredient hash')
    @allure.description('Negative test of the endpoint "Создание заказа" POST /api/orders.'
                        'Checks the failed attempt to create an order with wrong ingredient hash '
                        'and that request code 500')
    def test_order_creation_with_wrong_ingredients_hash_failed(self, create_user):
        payload = {"ingredients": ["thewrongesthashever"]}
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.post(Urls.create_order_url, data=payload, headers=headers)
        assert response.status_code == 500, f'Instead of code 500 received code {response.status_code}'