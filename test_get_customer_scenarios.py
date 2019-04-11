import requests
import helperIVRKit as IVR
import connectors
from devconfig import setUpConfig


data = setUpConfig()
customer_id = data['customer_id']


# valid - 200
def test_get_scenarios():
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_scenarios(bearer_token, customer_id)
    assert r.status_code == 206
    response = r.json()
    assert response != []


def test_get_scenarios_for_not_exist_customer():
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_scenarios(bearer_token, '9999999999')
    assert r.status_code == 400


def test_get_scenarios_with_invalid_customer_input():
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_scenarios(bearer_token, 'vcz')
    assert r.status_code == 400



