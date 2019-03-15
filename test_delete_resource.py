import helperIVRKit as IVR
import connectors
import random
import pytest
from devconfig import setUpConfig
from helperIVRKit import random_generator

data = setUpConfig()


# Может падать, так как некоторые номера могут быть уже в порта из NMS
def test_delete_resource_to_customer():
    params = {
        "orderName": random_generator(255),
        "orderDescription": random_generator(255),
        "customerId": "10774",
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
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_customer_numbers(bearer_token, params["customerId"])
    assert r.status_code == 200
    response = r.json()
    id_number = 0
    for number in response:
        if number['number'] == params["orderItemNumber"]:
            id_number = number["id"]
            break
    r = IVR.delete_customer_numbers(data['login'], data['password'], params["customerId"], id_number)
    assert r.status_code == 204


def test_delete_resource_with_wrong_id():
    ids = ['194191919529251', 'fdasv', '1']
    customer_id = '10774'
    r = IVR.delete_customer_numbers(data['login'], data['password'], customer_id, ids[0])
    assert r.status_code == 404
    r = IVR.delete_customer_numbers(data['login'], data['password'], customer_id, ids[1])
    assert r.status_code == 400
    r = IVR.delete_customer_numbers(data['login'], data['password'], customer_id, ids[2])
    assert r.status_code == 403
