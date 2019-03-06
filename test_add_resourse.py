import helperIVRKit as IVR
import time
import connectors
import random
from devconfig import setUpConfig

data = setUpConfig()


def test_add_resource_to_customer():
    number = IVR.get_random_number_for_reserve()
    query = connectors.search_record_postgres('SELECT cmgtc.id from customer_mgt.customer as cmgtc '
                                               'LEFT JOIN customer_mgt.characteristic as cmc '
                                               'ON cmgtc.id = cmc.characteristic_customer_id '
                                               'WHERE cmgtc.status = %(status)s and cmc.name = \'billingId\'',
                                              {'status': 'active'})
    random_record = random.choice(query)
    id = random_record[0]
    params = {
        "orderName": "TestPizzaQZ",
        "orderDescription": "dsa",
        "customerId": str(id),
        "orderItemNumber": str(number),
        "orderItemDescription": "testbuy"
    }
    print(str(id), str(number))
    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 201
    response = r.json()
    assert params == response


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
