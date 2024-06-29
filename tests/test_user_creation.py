import requests
import allure
import pytest

from data import Urls, Commondata


class TestUserCreation:

    @allure.title('Test of successful creation of a user')
    @allure.description('Positive test of the endpoint "Создание пользователя" POST /api/auth/register. '
                        'Checks that a user can be created, that response body contains all required fields, '
                        'and that a successful request returns "success": true')
    def test_successful_user_creation(self, create_user):
        response = create_user[0]
        assert response.status_code == 200, f'Failed to create new user, code {response.status_code}'
        assert response.json().get('success') is True, 'Field "success" is not True in the response body'
        assert 'user' in response.json(), 'Field "user" is missing in the response body'
        assert 'accessToken' in response.json(), 'Field "accessToken" is missing in the response body'
        user_data = response.json()['user']
        assert 'email' in user_data, 'Field "email" is missing in the "user" field of the response body'
        assert 'name' in user_data, 'Field "name" is missing in the "user" field of the response body'
        assert 'refreshToken' in response.json(), 'Field "refreshToken" is missing in the response body'

    @allure.title('Test of failed attempt to create a repeating user')
    @allure.description('Negative test of the endpoint "Создание пользователя" POST /api/auth/register.'
                        'Checks impossibility of creation of repeating user, '
                        'that response body contains all required fields, '
                        'and that request returns "success": false')
    def test_creation_repeating_user_failed(self, create_user):
        repeating_user_payload = {
            "email": f'{create_user[1]}',
            "password": Commondata.test_user_password,
            "name": Commondata.test_user_name
        }
        response = requests.post(Urls.register_url, data=repeating_user_payload)
        assert response.status_code == 403, f'Instead of an error code 403 received code {response.status_code}'
        assert response.json().get('success') is False, 'Field "success" is not False in the response body'
        assert response.json()['message'] == 'User already exists', f'Error message contains wrong text'

    @allure.title('Test of failed attempt to create a user with missing fields')
    @allure.description('Negative test of the endpoint "Создание пользователя" POST /api/auth/register.'
                        'Parameterized test, checks impossibility of creation of a user, '
                        'when any of the mandatory fields is missing, '
                        'and that request returns "success": false')
    @pytest.mark.parametrize('payload', Commondata.creation_missing_fields)
    def test_creation_user_with_any_missing_field_failed(self, payload):
        response = requests.post(Urls.register_url, data=payload)
        assert response.status_code == 403, f'Instead of an error code 403 received code {response.status_code}'
        assert response.json().get('success') is False, 'Field "success" is not False in the response body'
        assert response.json()['message'] == 'Email, password and name are required fields', \
            f'Error message contains wrong text'