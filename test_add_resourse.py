import helperIVRKit as IVR
import time
import connectors
import random
import pytest
from devconfig import setUpConfig

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
        "orderName": IVR.random_generator(),
        "orderDescription": IVR.random_generator(),
        "customerId": str(id),
        "orderItemNumber": str(number),
        "orderItemDescription": IVR.random_generator()
    }
    print(str(id), str(number))
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
# def test_add_invalid_to_customer():
#     number = IVR.get_random_number_for_reserve()
#     params = {
#         "orderName": "TestPizza",
#         "orderDescription": "sad",
#         "customerId": "10712",
#         "orderItemNumber": str(number) + '1',
#         "orderItemDescription": "wrongbuy"
#     }
#     r = IVR.add_resource(data['login'], data['password'], params)
#     assert r.status_code == 404


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


def test_max_length_OrderName():
    number = IVR.get_random_number_for_reserve()
    params = {
        "orderName": "",
        "orderDescription": "w1421124",
        "customerId": "4wres587564sd",
        "orderItemNumber": str(number),
        "orderItemDescription": "wrongbuy"
    }
    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 400


def test_add_resource_without_customerId():
    number = IVR.get_random_number_for_reserve()
    params = {
        "orderName": "TestPizza",
        "orderDescription": str(int(time.time())),
        "customerId": "",
        "orderItemNumber": str(number) + '1',
        "orderItemDescription": "wrongbuy"
    }
    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 400
