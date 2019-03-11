import requests
import random
import string
from devconfig import setUpConfig

data = setUpConfig()


# def set_env(cmdopt):
#     if cmdopt == 'env':
#         data = setUpConfig()
#     elif cmdopt == 'pp':
#         data =setUpConfig()
#     elif cmdopt == 'pp':
#         data = setUpConfig()


def take_token(login, password):
    base_url = data['ivr_url'] + '/token'
    headers = {'Content-Type': 'application/json'}
    params = {
        'login': login,
        'password': password
    }
    r = requests.post(base_url, headers=headers, json=params)
    assert r.status_code == 200
    response = r.json()
    return response['token']


def create_customer(token, params):
    base_url = data['ivr_url'] + '/customers'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token}
    r = requests.post(base_url, headers=headers, json=params)
    return r


def get_numbers(headers, params):
    base_url = data['ivr_url'] + '/number'
    r = requests.get(base_url, headers=headers, params=params)
    return r


def get_random_number_for_reserve():
    bearer_token = take_token(data['login'], data['password'])
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token,
               'Range': 'numbers=1-10'}
    params = {
        'category': 'REGULAR',
        'owner': 'MTT',
        'regionCode': 'MOW',
        'type': 'ABC',
        # 'mask': random.choice(mask)
    }
    r = get_numbers(headers=headers, params=params)
    assert r.status_code == 206
    response = r.json()
    number = (random.choice(response))
    assert number != {}
    return number["number"]


def get_filter(login, password):
    bearer_token = take_token(login, password)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    base_url = data['ivr_url'] + '/filters'
    r = requests.get(base_url, headers=headers)
    return r


def reserve_number(login, password, params):
    bearer_token = take_token(login, password)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    base_url = data['ivr_url'] + '/number/reserve'
    r = requests.post(base_url, headers=headers, json=params)
    return r


def delete_reserved_number(login, password, params):
    bearer_token = take_token(login, password)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    base_url = data['ivr_url'] + '/number/reserve'
    r = requests.delete(base_url, headers=headers, json=params)
    return r


def add_resource(login, password, params):
    bearer_token = take_token(login, password)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    base_url = data['ivr_url'] + '/numbers'
    r = requests.post(base_url, headers=headers, json=params)
    return r


def get_customer_resource(login, password, id):
    bearer_token = take_token(login, password)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    base_url = data['ivr_url'] + '/customers/' + id + '/numbers'
    r = requests.get(base_url, headers=headers)
    return r


def random_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def get_customer_numbers(bearer_token, id):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    base_url = data['ivr_url'] + '/customers/' + str(id) + '/numbers'
    r = requests.get(base_url, headers=headers)
    return r
