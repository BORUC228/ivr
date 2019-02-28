import time
import random
import requests
import helperIVRKit as IVR
import Connectors
from devconfig import setUpConfig

data = setUpConfig()


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
    assert new_customer == response

    # Проверка наличия кастомера в Porta
    r = Connectors.get_customer_info(response['name'])
    assert r is not False
    assert new_customer['name'] == r['customer_info']['name']

    # Проверка наличия кастомера в базе CMAPI
    r = IVR.search_record_postgres(response['name'])
    assert response['name'] == r.name


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
    r = pC.getCustomerInfo(new_customer['name'])
    assert r == {}

    # Проверка наличия кастомера в базе CMAPI
    r = IVR.search_record_postgres(new_customer['name'])
    assert r is None


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
    base_url = data['ivr_url'] + '/token'
    headers = {'Content-Type': 'application/json'}
    r = requests.post(base_url, headers=headers, json=new_customer)
    assert r.status_code == 401

    # Проверка наличия кастомера в Porta
    r = pC.getCustomerInfo(new_customer['name'])
    assert r == {}

    # Проверка наличия кастомера в базе CMAPI
    r = IVR.search_record_postgres(new_customer['name'])
    assert r is None
