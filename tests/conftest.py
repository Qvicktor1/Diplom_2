import pytest
import requests
import random
import string

from data import Urls, Commondata


@pytest.fixture
def create_user():
    letters = string.ascii_lowercase
    login = ''.join(random.choice(letters) for _ in range(10)) + '@ya.ru'
    payload = {"email": f'{login}',
               "password": Commondata.test_user_password,
               "name": Commondata.test_user_name
               }
    response = requests.post(Urls.register_url, data=payload)
    access_token = response.json().get("accessToken")
    yield response, login, access_token
    headers = {'Authorization': f'{access_token}'}
    requests.delete(Urls.delete_user_url, headers=headers)


@pytest.fixture
def create_n_orders(create_user, request=3):
    orders_to_create = request
    payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6d"]}
    headers = {'Authorization': f'{create_user[2]}'}
    for order in range(orders_to_create):
        requests.post(Urls.create_order_url, data=payload, headers=headers)


