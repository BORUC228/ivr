import requests
from devconfig import setUpConfig

data = setUpConfig()


def test_take_token_with_valid_auth():
    base_url = data['ivr_url'] + '/token'
    headers = {'Content-Type': 'application/json'}
    params = {
        'login': data['login'],
        'password': data['password']
    }
    r = requests.post(base_url, headers=headers, json=params)
    assert r.status_code == 200
    response = r.json()
    assert 'token' in response
    assert response['token'] != ''


def test_take_token_with_invalid_auth():
    base_url = data['ivr_url'] + '/token'
    headers = {'Content-Type': 'application/json'}
    params = {
        'login': data['bad_login'],
        'password': data['password']
    }
    r = requests.post(base_url, headers=headers, json=params)
    assert r.status_code == 401
    response = r.json()
    assert response['name'] == 'Unauthorized'
    assert response['message'] == 'login or password is invalid'


def test_take_token_with_missing_password():
    base_url = data['ivr_url'] + '/token'
    headers = {'Content-Type': 'application/json'}
    params = {
        'login': data['login'],
        'password': ''
    }
    r = requests.post(base_url, headers=headers, json=params)
    assert r.status_code == 401
    response = r.json()
    assert response['name'] == 'Unauthorized'
    assert response['message'] == 'login or password is invalid'


def test_take_token_with_missing_login():
    base_url = data['ivr_url'] + '/token'
    headers = {'Content-Type': 'application/json'}
    params = {
        'login': '',
        'password': data['password']
    }
    r = requests.post(base_url, headers=headers, json=params)
    assert r.status_code == 401
    response = r.json()
    assert response['name'] == 'Unauthorized'
    assert response['message'] == 'login or password is invalid'
