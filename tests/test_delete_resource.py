from tests import helperIVRKit as IVR
from tests.devconfig import setUpConfig
from tests.helperIVRKit import random_generator

data = setUpConfig()
customer_id = '10777'


# Может падать, так как некоторые номера могут быть уже в порта из NMS
def test_delete_resource_to_customer():
    params = {
        "orderName": random_generator(255),
        "orderDescription": random_generator(255),
        "orderItemNumber": random_generator(128),
        "orderItemDescription": random_generator(255)
    }
    r = IVR.add_resource(data['login'], data['password'], customer_id, params)
    assert r.status_code == 201
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_customer_numbers(bearer_token, customer_id)
    assert r.status_code == 206
    response = r.json()
    id_number = 0
    for number in response:
        if number['number'] == params["orderItemNumber"]:
            id_number = number["id"]
            break
    r = IVR.delete_customer_numbers(data['login'], data['password'], customer_id, id_number)
    assert r.status_code == 204
    r = IVR.get_customer_numbers(bearer_token, customer_id)
    response = r.json()
    for number in response:
        if number['number'] == params["orderItemNumber"]:
            assert 1 == 0
        break
    r = IVR.delete_customer_numbers(data['login'], data['password'], customer_id, id_number)
    assert r.status_code == 404


def test_delete_resource_with_wrong_id():
    ids = ['194191919529251', 'fdasv', '1']
    r = IVR.delete_customer_numbers(data['login'], data['password'], customer_id, ids[0])
    assert r.status_code == 404
    r = IVR.delete_customer_numbers(data['login'], data['password'], customer_id, ids[1])
    assert r.status_code == 400
    r = IVR.delete_customer_numbers(data['login'], data['password'], customer_id, ids[2])
    assert r.status_code == 403
