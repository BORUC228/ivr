import requests
import helperIVRKit as IVR
import connectors
from devconfig import setUpConfig

data = setUpConfig()


def test_get_existing_customers():
    bearer_token = IVR.take_token(data['login'], data['password'])
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    base_url = data['ivr_url'] + '/customers'
    r = requests.get(base_url, headers=headers)
    assert r.status_code == 206
    response = r.json()
    id = response[-1]['id']

    # Проверка наличия кастомера в базе CMAPI
    r = connectors.search_record_postgres('SELECT * FROM customer_mgt.customer_mgt.customer WHERE id = %(id)s',
                                          {'id': id})
    assert r != []
    base_url = data['ivr_url'] + '/customers?id=510'
    r = requests.get(base_url, headers=headers)
    assert r.status_code == 206
    response = r.json()
    assert len(response) == 1


def test_get_not_existing_customer():
    bearer_token = IVR.take_token(data['login'], data['password'])
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    base_url = data['ivr_url'] + '/customers?id=9999999'
    r = requests.get(base_url, headers=headers)
    assert r.status_code == 404
    id = '999999'

    # Проверка наличия кастомера в базе CMAPI
    r = connectors.search_record_postgres('SELECT * FROM customer_mgt.customer_mgt.customer WHERE id = %(id)s',
                                          {'id': id})
    assert r == []


