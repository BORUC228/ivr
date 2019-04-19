from tests import helperIVRKit as IVR
import json
import pytest
from tests.devconfig import setUpConfig
from tests.helperIVRKit import random_generator

data = setUpConfig()
bearer_token = IVR.take_token(data['login'], data['password'])


def test_create_scenario():
    params = {
        'title': random_generator(size=63),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States']))
    }
    r = IVR.create_scenario(bearer_token, data['customer_id'], params)
    assert r.status_code == 201
    response = r.json()
    assert response['title'] == params['title']
    assert response['comment'] == params['comment']
    scenario = IVR.get_scenarios(bearer_token, data['customer_id'])
    assert scenario.status_code == 206


def test_create_scenario_with_restricted_params():
    params = [
        {
            'title': random_generator(size=129),
            'comment': 'HEH',
            'States': json.loads(json.JSONEncoder().encode(data['States']))
        },
        {
            'title': random_generator(size=128),
            'comment': random_generator(size=129),
            'States': json.loads(json.JSONEncoder().encode(data['States']))
        },
    ]
    r = IVR.create_scenario(bearer_token, data['customer_id'], params)
    assert r.status_code == 400


def test_not_unique_scenario_title():
    params = {
        'title': random_generator(size=128),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States']))
    }
    r = IVR.create_scenario(bearer_token, data['customer_id'], params)
    assert r.status_code == 201
    r = IVR.create_scenario(bearer_token, data['customer_id'], params)
    assert r.status_code == 409


@pytest.mark.parametrize('params', [
    pytest.param({
        'title': '',
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States']))
    }, id='without title'),
    pytest.param(
        {
            'title': random_generator(size=128),
            'comment': 'sdfa',
            'States': ''
        }, id='without state')
])
def test_creating_with_empty_params(params):
    r = IVR.create_scenario(bearer_token, data['customer_id'], params)
    assert r.status_code == 400


def test_not_exist_customer_id():
    params = {
        'title': random_generator(size=128),
        'comment': 'HEH',
        'States': data['States']
    }
    r = IVR.create_scenario(bearer_token, '7897987987987987978', params)
    assert r.status_code == 400
    response = r.json()
    assert response['message'] == 'customer doesn\'t exist'

