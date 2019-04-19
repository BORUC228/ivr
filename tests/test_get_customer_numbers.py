from tests import helperIVRKit as IVR
from tests.devconfig import setUpConfig

data = setUpConfig()
bearer_token = IVR.take_token(data['login'], data['password'])

def test_customer_with_numbers():
    r = IVR.get_customer_numbers(bearer_token, data['customer_id'])
    assert r.status_code == 206
    response = r.json()
    assert response is not None


def test_customer_without_numbers():
    r = IVR.get_customer_numbers(bearer_token, '10772')
    assert r.status_code == 206
    response = r.json()
    assert response is None


def test_not_existing_customer():
    r = IVR.get_customer_numbers(bearer_token, '999999')
    assert r.status_code == 400


def test_customer_with_invalid_id():
    r = IVR.get_customer_numbers(bearer_token, 'ballon')
    assert r.status_code == 400


