import helperIVRKit as IVR
import connectors
import random
import pytest
from devconfig import setUpConfig
from helperIVRKit import random_generator

data = setUpConfig()


# Может падать, так как некоторые номера могут быть уже в порта из NMS
def test_add_resource_to_customer():
    number = IVR.get_random_number_for_reserve()
    query = connectors.search_record_postgres('SELECT cmgtc.id,cmgtc.name from customer_mgt.customer as cmgtc '
                                              'LEFT JOIN customer_mgt.characteristic as cmc '
                                              'ON cmgtc.id = cmc.characteristic_customer_id '
                                              'WHERE cmgtc.status = %(status)s and cmc.name = \'billingId\'',
                                              {'status': 'active'})
    random_record = random.choice(query)
    id = random_record[0]
    customer_name = random_record[1]
    params = {
        "orderName": random_generator(255),
        "orderDescription": random_generator(255),
        "customerId": str(id),
        "orderItemNumber": random_generator(128),
        "orderItemDescription": IVR.random_generator(255)
    }

    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 201
    if r.status_code == 500:
        response = r.json()
        print(response['message'])
    response = r.json()
    assert params == response

    # Проверка того, что ресурс добавился в Porta
    r = connectors.get_account_info(str(number))
    assert r['account_info']['customer_name'] == customer_name
    # Проверка того, что ресурс добавился в ResourceMGTAPI
    query = connectors.search_record_postgres(
        'SELECT billing_id FROM customer_mgt.resource_management.resource_number WHERE dialed_number = %(number)s',
        {'number': str(number)})
    random_record = random.choice(query)
    billing_id = random_record[0]


@pytest.mark.xfail(run=False)
def test_invalid_customer_Id():
    number = IVR.get_random_number_for_reserve()
    params = {
        "orderName": "trewt",
        "orderDescription": "sad",
        "customerId": "122ds2321",
        "orderItemNumber": str(number),
        "orderItemDescription": "wrongbuy"
    }
    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 400


@pytest.mark.xfail(run=False)
def test_missing_required_params():
    number = IVR.get_random_number_for_reserve()
    params = [
        {
            "orderName": "",
            "customerId": "4wres587564sd",
            "orderItemNumber": str(number),
            "orderItemDescription": "wrongbuy"
        },
        {
            "orderName": "vsa",
            "customerId": "",
            "orderItemNumber": str(number),
            "orderItemDescription": "wrongbuy"
        },
        {
            "orderName": "vsa",
            "customerId": "10774",
            "orderItemNumber": "",
            "orderItemDescription": "wrongbuy"
        },
        {
            "orderName": "vsa",
            "customerId": "10774",
            "orderItemNumber": str(number),
            "orderItemDescription": ""
        }
    ]
    for case in params:
        r = IVR.add_resource(data['login'], data['password'], case)
        assert r.status_code == 400


def test_unique_params():
    number = IVR.get_random_number_for_reserve()
    params = {
        "orderName": "zakzak",
        "customerId": "10774",
        "orderItemNumber": str(number) + '111',
        "orderItemDescription": "wrongbuy"
    }
    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 201
    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 500


def test_wrong_type_params():
    number = IVR.get_random_number_for_reserve()
    params = [
        {
            "orderName": 900,
            "customerId": "10774",
            "orderItemNumber": str(number),
            "orderItemDescription": "wrongbuy"
        },        {
            "orderName": "dsad",
            "customerId": 10774,
            "orderItemNumber": str(number),
            "orderItemDescription": "wrongbuy"
        },        {
            "orderName": "dsad",
            "customerId": "10774",
            "orderItemNumber": int(number),
            "orderItemDescription": "wrongbuy"
        },        {
            "orderName": "dsad",
            "customerId": "10774",
            "orderItemNumber": str(number),
            "orderItemDescription": 770
        }
    ]
    for case in params:
        r = IVR.add_resource(data['login'], data['password'], case)
        assert r.status_code == 400


def test_restricted_params():
    number = IVR.get_random_number_for_reserve()
    params = [
        {
            "orderName": random_generator(256),
            "orderDescription": "sad",
            "customerId": "10774",
            "orderItemNumber": str(number),
            "orderItemDescription": "wrongbuy"
        },        {
            "orderName": random_generator(255),
            "orderDescription": random_generator(256),
            "customerId": "10774",
            "orderItemNumber": str(number),
            "orderItemDescription": "wrongbuy"
        },        {
            "orderName": random_generator(100),
            "orderDescription": "ssad",
            "customerId": "10774",
            "orderItemNumber": random_generator(129),
            "orderItemDescription": "wrongbuy"
        },        {
            "orderName": random_generator(100),
            "orderDescription": "sad",
            "customerId": "10774",
            "orderItemNumber": str(number),
            "orderItemDescription": random_generator(256)
        }
    ]
    for case in params:
        r = IVR.add_resource(data['login'], data['password'], case)
        assert r.status_code == 400
