import helperIVRKit as IVR
import pprint
import json
from devconfig import setUpConfig
from helperIVRKit import random_generator

data = setUpConfig()


def test_create_scenario():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=63),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States']))
    }
    r = IVR.create_scenario(bearer_token, data['customer_id'], params)
    pprint.pprint(params)
    assert r.status_code == 201
    response = r.json()
    assert response['title'] == params['title']
    assert response['comment'] == params['comment']
    scenario = IVR.get_scenarios(bearer_token, data['customer_id'])
    assert scenario.status_code == 206
    response = r.json()
    assert response[-1]['title'] == params['title']


def test_create_scenario_with_restricted_params():
    bearer_token = IVR.take_token(data['login'], data['password'])
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
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=128),
        'comment': 'HEH',
        'States': json.loads(json.JSONEncoder().encode(data['States']))
    }
    r = IVR.create_scenario(bearer_token, data['customer_id'], params)
    assert r.status_code == 201
    r = IVR.create_scenario(bearer_token, data['customer_id'], params)
    assert r.status_code == 409
    # response = r.json()
    # assert response['message'] == 'unexpected protei response status ALREADY_EXIST'


def test_creating_with_empty_params():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = [
        {
            'title': '',
            'comment': 'HEH',
            'States': json.loads(json.JSONEncoder().encode(data['States']))
        },
        {
            'title': random_generator(size=128),
            'comment': '',
            'States': json.loads(json.JSONEncoder().encode(data['States']))
        },
        {
            'title': random_generator(size=128),
            'comment': 'sdfa',
            'States': ''
        },
    ]
    r = IVR.create_scenario(bearer_token, data['customer_id'], params)
    assert r.status_code == 400


def test_not_exist_customer_id():
    bearer_token = IVR.take_token(data['login'], data['password'])
    params = {
        'title': random_generator(size=128),
        'comment': 'HEH',
        'States': data['States']
    }
    r = IVR.create_scenario(bearer_token, '7897987987987987978', params)
    assert r.status_code == 400
    response = r.json()
    assert response['message'] == 'customer doesn\'t exist'

