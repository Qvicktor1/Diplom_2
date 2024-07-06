## Диплом Задание 2

Тесты API сервиса StellarBurger

### Файлы с тестами:
#### 1. test_user_creation.py 
<i>Проверяет ручку "Создание пользователя" POST /api/auth/register.</i>

Содержит тесты:
- test_successful_user_creation
- test_creation_repeating_courier_failed
- test_creation_repeating_user_failed
- test_creation_user_with_any_missing_field_failed


#### 2. test_user_login.py
<i>Проверяет ручку "Авторизация пользователя" POST /api/auth/login.</i>

Содержит тесты:
- test_successful_user_login
- test_login_with_any_wrong_field_failed


#### 3. test_change_user_data.py
<i>Проверяет ручку "Обновление данных пользователя" PATCH /api/auth/user.</i>

Содержит тесты:
- test_successful_user_data_change_with_auth
- test_failed_user_data_change_without_auth


#### 4. test_order_creation.py
<i>Проверяет ручку "Создание заказа" POST /api/v1/orders.</i>

Содержит тесты:
- test_order_creation_with_authorization_and_ingredients
- test_order_creation_without_authorization_failed
- test_order_creation_without_ingredients_failed
- test_order_creation_with_wrong_ingredients_hash_failed


#### 5. test_get_user_orders.py
<i>Проверяет ручку "Получение заказов конкретного пользователя" GET /api/orders.</i>

Содержит тесты:
- test_get_user_orders_with_authorization
- test_sorting_user_orders_with_authorization
- test_get_user_orders_without_authorization_failed


