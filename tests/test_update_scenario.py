from tests import helperIVRKit as IVR
import json
import pytest
from tests.devconfig import setUpConfig
from tests.helperIVRKit import random_generator

data = setUpConfig()
customer_a_id = data['customer_id']
customer_b_id = '10832'
customer_a_scenario = '440'
customer_b_scenario = '298'


@pytest.mark.update
def test_update_scenario():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=63),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States_4_update'])),
        'CommonScript': data['CommonScript']
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_a_scenario, params)
    assert r.status_code == 200
    response = r.json()
    assert response['title'] == params['title']
    assert response['CommonScript'] == params['CommonScript']


def test_update_scenario_with_restricted_params():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=129),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States_4_update'])),
        'CommonScript': data['CommonScript']
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_a_scenario, params)
    assert r.status_code == 400

'''
def test_empty_params():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=128),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States_4_update'])),
        'CommonScript': data['CommonScript']
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_a_id, params)
    assert r.status_code == 209
'''


def test_not_exist_customer_id():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=70),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States_4_update'])),
        'CommonScript': data['CommonScript']
    }
    r = IVR.update_scenario(bearer_token, '7979797777779', customer_a_scenario, params)
    assert r.status_code == 400
    response = r.json()
    assert response['message'] == 'customer doesn\'t exist'


def test_not_exist_scenario_id():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=70),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States_4_update'])),
        'CommonScript': data['CommonScript']
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, '1000000', params)
    assert r.status_code == 404
    response = r.json()
    assert response['message'] == 'resource not found'


def test_update_foreign_scenario():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=70),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States_4_update'])),
        'CommonScript': data['CommonScript']
    }
    r = IVR.update_scenario(bearer_token, customer_a_id, customer_b_scenario, params)
    assert r.status_code == 403
    response = r.json()
    assert response['message'] == 'access forbidden'
