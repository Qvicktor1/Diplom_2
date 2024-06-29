class Commondata:
    test_user_password = 'SuperStrongPassword'
    test_user_name = 'UserPro'
    creation_missing_fields = [
        {"password": 'SuperStrongPassword', "name": 'UserPro'},
        {"email": 'test_email@ya.ru', "name": 'UserPro'},
        {"email": 'test_email2@ya.ru', "password": 'SuperStrongPassword'}
    ]


class Urls:
    register_url = 'https://stellarburgers.nomoreparties.site/api/auth/register'
    login_url = 'https://stellarburgers.nomoreparties.site/api/auth/login'
    delete_user_url = 'https://stellarburgers.nomoreparties.site/api/auth/user'
    change_user_data_url = 'https://stellarburgers.nomoreparties.site/api/auth/user'
    create_order_url = 'https://stellarburgers.nomoreparties.site/api/orders'
    get_user_orders = 'https://stellarburgers.nomoreparties.site/api/orders'


