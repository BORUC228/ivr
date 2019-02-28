import requests
import psycopg2
import random
import psycopg2.extras
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


def search_record_postgres(customer_name):
    conn = psycopg2.connect(dbname=data['postgres']['dbname'], user=data['postgres']['user'],
                            password=data['postgres']['password'], host=data['postgres']['host'])
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute('SELECT * FROM customer_mgt.customer_mgt.customer WHERE name = %(name)s',
                   {'name': customer_name})
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    return record


def get_numbers(headers, params):
    base_url = data['ivr_url'] + '/number'
    r = requests.get(base_url, headers=headers, params=params)
    return r


def get_random_number_for_reserve():
    base_url = data['ivr_url'] + '/number'
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
    return str(response[0]['number'])


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
