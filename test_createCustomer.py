import time
import random
import requests
import helperIVRKit as IVR
import connectors
from devconfig import setUpConfig
from helperIVRKit import random_generator

data = setUpConfig()


# valid create - 201
def test_create_customer_with_valid_token():
    bearer_token = IVR.take_token(data['login'], data['password'])
    new_customer = {
        'name': 'testIVR_' + str(int(time.time())),
        'status': '1',
        'description': '1',
        'login': 'testIVR_' + str(int(time.time())),
        'password': 'pass_' + str(random.uniform(1, 2000000)),
        'email': str(int(time.time())) + '@gg.ru',
        'phone': '79777777777'
    }
    r = IVR.create_customer(bearer_token, new_customer)
    assert r.status_code == 201
    response = r.json()
    assert response['id']
    assert new_customer['name'] == response['name']
    assert new_customer['status'] == response['status']
    assert new_customer['description'] == response['description']
    assert new_customer['login'] == response['login']
    assert new_customer['password'] == response['password']
    assert new_customer['email'] == response['email']
    assert new_customer['phone'] == response['phone']
    # Проверка наличия кастомера в Porta
    r = connectors.get_customer_info(response['name'])
    assert r is not False
    assert new_customer['name'] == r['customer_info']['name']

    # Проверка наличия кастомера в базе CMAPI
    # r = connectors.search_record_postgres('SELECT * FROM customer_mgt.customer_mgt.customer WHERE name = %(name)s',
    #                {'name': new_customer['name']})
    # assert response['name'] == r[0][4]


def test_create_customer_with_required_params_only():
    bearer_token = IVR.take_token(data['login'], data['password'])
    new_customer = {
        'name': 'testIVR_' + str(int(time.time())),
        'status': '1',
        'login': 'testIVR_' + str(int(time.time())),
        'password': 'pass_' + str(random.uniform(1, 2000000)),
        'email': str(int(time.time())) + '@gg.ru',
        'phone': '79777777777'
    }
    r = IVR.create_customer(bearer_token, new_customer)
    assert r.status_code == 201
    response = r.json()
    assert response['id']
    assert new_customer['name'] == response['name']
    assert new_customer['status'] == response['status']
    assert new_customer['login'] == response['login']
    assert new_customer['password'] == response['password']
    assert new_customer['email'] == response['email']
    assert new_customer['phone'] == response['phone']
    # Проверка наличия кастомера в Porta
    r = connectors.get_customer_info(response['name'])
    assert r is not False
    assert new_customer['name'] == r['customer_info']['name']
    # Проверка наличия кастомера в базе CMAPI
    r = connectors.search_record_postgres('SELECT * FROM customer_mgt.customer_mgt.customer WHERE name = %(name)s',
                   {'name': new_customer['name']})
    assert response['name'] == r[0][4]


# wrong token - 401
def test_create_customer_with_invalid_token():
    bearer_token = 's2O3D9R5VnYpot9b6kQ='
    new_customer = {
        'name': 'testIVR_' + str(int(time.time())),
        'status': '1',
        'description': '1',
        'login': 'testIVR_' + str(int(time.time())),
        'password': 'pass_' + str(random.uniform(1, 2000000)),
        'email': str(int(time.time())) + '@gg.ru',
        'phone': '77777777777'
    }
    r = IVR.create_customer(bearer_token, new_customer)
    assert r.status_code == 401

    # Проверка наличия кастомера в Porta
    r = connectors.get_customer_info(new_customer['name'])
    assert r == {}

    # Проверка наличия кастомера в базе CMAPI
    r = connectors.search_record_postgres('SELECT * FROM customer_mgt.customer_mgt.customer WHERE name = %(name)s',
                   {'name': new_customer['name']})
    assert r == []


# without token - 401
def test_create_customer_without_token():
    new_customer = {
        'name': 'testIVR_' + str(int(time.time())),
        'status': '1',
        'description': '1',
        'login': 'testIVR_' + str(int(time.time())),
        'password': 'pass_' + str(random.uniform(1, 2000000)),
        'email': str(int(time.time())) + '@gg.ru',
        'phone': '77777777777'
    }
    base_url = data['ivr_url'] + '/customers'
    headers = {'Content-Type': 'application/json'}
    r = requests.post(base_url, headers=headers, json=new_customer)
    assert r.status_code == 401
    response = r.json()
    assert response['message'] == 'token header is missing'


# without required params - 400
def test_create_customer_without_required_params():
    bearer_token = IVR.take_token(data['login'], data['password'])
    data_customer = [
        {
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '77777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '77777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '77777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '77777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'phone': '77777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru'
        },
        # пустые значения
        {
            'name': '',
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '79777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '',
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '79777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': '',
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '79777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': '',
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '79777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': '',
            'phone': '79777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': ''
        }
    ]
    for case in data_customer:
        r = IVR.create_customer(bearer_token, params=case)
        assert r.status_code == 400


def test_create_customer_with_restricted_params():
    bearer_token = IVR.take_token(data['login'], data['password'])
    data_customer = [
        {
            'name': random_generator(42),
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '79777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': random_generator(256),
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '79777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': random_generator(256),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '79777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': random_generator(256),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': '79777777777'
        },
        {
            'name': 'testIVR_' + str(int(time.time())),
            'status': '1',
            'login': 'testIVR_' + str(int(time.time())),
            'password': 'pass_' + str(random.uniform(1, 2000000)),
            'email': str(int(time.time())) + '@gg.ru',
            'phone': random_generator(256, "1234567980")
        },
    ]
    for case in data_customer:
        r = IVR.create_customer(bearer_token, params=case)
        assert r.status_code == 500

