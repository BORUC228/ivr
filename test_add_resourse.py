import helperIVRKit as IVR
import time
from devconfig import setUpConfig

data = setUpConfig()


def test_add_resource_to_customer():
    number = IVR.get_random_number_for_reserve()
    params = {
        "orderName": "TestPizza",
        "orderDescription": str(int(time.time())),
        "customerId": "10712",
        "orderItemNumber": str(number),
        "orderItemDescription": "testbuy"
    }
    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 200
    response = r.json()
    assert params == response


def test_add_invalid_to_customer():
    number = IVR.get_random_number_for_reserve()
    params = {
        "orderName": "TestPizza",
        "orderDescription": str(int(time.time())),
        "customerId": "10712",
        "orderItemNumber": str(number) + '1',
        "orderItemDescription": "wrongbuy"
    }
    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 404


def test_invalid_customer_Id():
    number = IVR.get_random_number_for_reserve()
    params = {
        "orderName": "TestPizza",
        "orderDescription": str(int(time.time())),
        "customerId": "4wres587564sd",
        "orderItemNumber": str(number),
        "orderItemDescription": "wrongbuy"
    }
    r = IVR.add_resource(data['login'], data['password'], params)
    assert r.status_code == 400


def test_max_length_OrderName():
    number = IVR.get_random_number_for_reserve()
    params = {
        "orderName": "",
        "orderDescription": str(int(time.time())),
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
    assert r.status_code == 404
