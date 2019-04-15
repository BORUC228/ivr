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


# invalid auth, missing password, missing login, missing login and password  - 401
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
    params = [
        {
            'login': data['login'],
            'password': ''
        },
        {
            'login': '',
            'password': data['password']
        },
        {
            'login': '',
            'password': ''
        }
    ]
    for case in params:
        r = requests.post(base_url, headers=headers, json=case)
        assert r.status_code == 400
