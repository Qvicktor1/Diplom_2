import requests
import allure
import pytest

from data import Urls, Commondata


class TestUserLogin:

    @allure.title('Test of successful user login')
    @allure.description('Positive test of the endpoint "Авторизация пользователя" POST /api/auth/login. '
                        'Checks that a user can be created, that response body contains all required fields, '
                        'and that a successful request returns "success": true')
    def test_successful_user_login(self, create_user):
        payload = {"email": create_user[1],
                   "password": Commondata.test_user_password
                   }
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.post(Urls.login_url, data=payload, headers=headers)
        assert response.status_code == 200, f'Failed to login user, code {response.status_code}'
        assert response.json().get('success') is True, 'Field "success" is not True in the response body'
        assert 'user' in response.json(), 'Field "user" is missing in the response body'
        assert 'accessToken' in response.json(), 'Field "accessToken" is missing in the response body'
        user_data = response.json()['user']
        assert 'email' in user_data, 'Field "email" is missing in the "user" field of the response body'
        assert 'name' in user_data, 'Field "name" is missing in the "user" field of the response body'
        assert 'refreshToken' in response.json(), 'Field "refreshToken" is missing in the response body'

    @allure.title('Test of failed attempt to login with the wrong fields')
    @allure.description('Negative test of the endpoint "Авторизация пользователя" POST /api/auth/login.'
                        'Parameterized test, checks impossibility of authorization '
                        'when any of the mandatory fields is wrong')
    @pytest.mark.parametrize("wrong_field", ["email", "password"])
    def test_login_with_any_wrong_field_failed(self, create_user, wrong_field):
        payload = {
            "email": create_user[0],
            "password": Commondata.test_user_password
        }
        payload[wrong_field] = f'{payload[wrong_field]}a'
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.post(Urls.login_url, data=payload, headers=headers)
        assert response.status_code == 401, f'Instead of an error code 401 received code {response.status_code}'
        assert response.json().get('success') is False, 'Field "success" is not False in the response body'
        assert response.json()['message'] == 'email or password are incorrect', f'Error message contains wrong text'