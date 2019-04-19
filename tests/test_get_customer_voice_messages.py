from tests import helperIVRKit as IVR
from tests.devconfig import setUpConfig


data = setUpConfig()
customer_id = data['customer_id']
bearer_token = IVR.take_token(data['login'], data['password'])


def test_get_voice_messages():
    r = IVR.get_voice_messages(bearer_token, customer_id)
    assert r.status_code == 206
    response = r.json()
    assert response != []


def test_get_voice_messages_for_not_exist_customer():
    r = IVR.get_voice_messages(bearer_token, '9999999999')
    assert r.status_code == 400


def test_get_voice_messages_with_invalid_customer_input():
    r = IVR.get_voice_messages(bearer_token, 'vcz')
    assert r.status_code == 400


def test_get_customer_voice_messages_without_voice_message():
    r = IVR.get_voice_messages(bearer_token, '10847')
    assert r.status_code == 206



