import requests
import allure
import pytest

from data import Urls, Commondata


class TestChangeUserData:

    @allure.title('Test of successful user data change with authorization')
    @allure.description('Positive test of the endpoint "Обновление данных пользователя" PATCH /api/auth/user. '
                        'Parameterized test checks that a user data can be changed with authorization, '
                        'that response body contains all required fields, '
                        'and that a successful request returns "success": true')
    @pytest.mark.parametrize("changed_field", ["email", "password", "name"])
    def test_successful_user_data_change_with_auth(self, create_user, changed_field):
        payload = {"email": create_user[1],
                   "password": Commondata.test_user_password,
                   "name": Commondata.test_user_name
                   }
        payload[changed_field] = f'{payload[changed_field]}a'
        headers = {'Authorization': f'{create_user[2]}'}
        response = requests.patch(Urls.change_user_data_url, data=payload, headers=headers)
        assert response.status_code == 200, f'Failed to change user data, code {response.status_code}'
        assert response.json().get('success') is True, 'Field "success" is not True in the response body'
        assert 'user' in response.json(), 'Field "user" is missing in the response body'
        user_data = response.json()['user']
        assert 'email' in user_data, 'Field "email" is missing in the "user" field of the response body'
        assert 'name' in user_data, 'Field "name" is missing in the "user" field of the response body'

    @allure.title('Test of failed attempt to change user data without authorization')
    @allure.description('Negative test of the endpoint "Обновление данных пользователя" PATCH /api/auth/user. '
                        'Parameterized test, checks that a user data can not be changed without authorization, '
                        'that response body contains all required fields, '
                        'and that a request returns "success": false')
    @pytest.mark.parametrize("changed_field", ["email", "password", "name"])
    def test_failed_user_data_change_without_auth(self, create_user, changed_field):
        payload = {"email": create_user[1],
                   "password": Commondata.test_user_password,
                   "name": Commondata.test_user_name
                   }
        payload[changed_field] = f'{payload[changed_field]}a'
        response = requests.patch(Urls.change_user_data_url, data=payload)
        assert response.status_code == 401, f'Instead of an error code 401 received code {response.status_code}'
        assert response.json().get('success') is False, 'Field "success" is not False in the response body'
        assert response.json()['message'] == 'You should be authorised', f'Error message contains wrong text'