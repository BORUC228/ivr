import helperIVRKit as IVR
from devconfig import setUpConfig
from helperIVRKit import random_generator

data = setUpConfig()
customer_a_id = data['customer_id']
customer_b_id = '10770'
customer_a_scenario = '102'
customer_b_scenario = '106'


# valid update - 200
def test_update_scenario():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=128)
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_a_scenario, params)
    assert r.status_code == 200
    response = r.json()
    assert response['title'] == params['title']


def test_update_scenario_with_restricted_params():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=129)
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_a_id, params)
    assert r.status_code == 400


# Подумать над проверкой
def test_not_unique_scenario_title():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=128)
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_a_scenario, params)
    assert r.status_code == 200
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_a_scenario, params)
    assert r.status_code == 500
    response = r.json()
    assert response['message'] == 'unexpected protei response status ALREADY_EXIST'


def test_empty_title():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': ''
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_a_id, params)
    assert r.status_code == 400


def test_not_exist_customer_id():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=25)
    }
    r = IVR.update_scenario(bearer_token, '7979797777779', customer_a_scenario, params)
    assert r.status_code == 400
    response = r.json()
    assert response['message'] == 'customer doesn\'t exist'


def test_not_exist_scenario_id():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=25)
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, '7979797979797979797979797', params)
    assert r.status_code == 400
    response = r.json()
    assert response['message'] == 'scenario doesn\'t exist'


def test_update_foreign_scenario():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=25)
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_b_scenario, params)
    assert r.status_code == 403
    response = r.json()
    assert response['message'] == 'Access forbiden'
