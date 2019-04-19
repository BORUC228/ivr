import time
import pytest
from tests import helperIVRKit as IVR
from tests.devconfig import setUpConfig
from tests.connectors import get_number_info

data = setUpConfig()


def test_reserve_and_unreserve_correct_number():
    number = IVR.get_random_number_for_reserve()
    params = {
        'number': str(number),
        'period': 600
    }
    r = IVR.reserve_number(data['login'], data['password'], params)
    assert r.status_code == 201
    response = r.json()
    assert 'reserved_uid' in response[0]
    reserved_uid = response[0]['reserved_uid']
    r = get_number_info(number)
    assert r['result'][0]['state_name'] == "RESERVED"
    delete_params = {
        'number': str(number),
        'reserved_uid': reserved_uid
    }
    r = IVR.delete_reserved_number(data['login'], data['password'], delete_params)
    assert r.status_code == 204
    r = get_number_info(number)
    assert r['result'][0]['state_name'] == "FREE"


def test_reserve_broken_number():
    number = IVR.get_random_number_for_reserve()
    params_400 = [
        {
            'number': int(number),
            'period': 600
        },
        {
            'number': str(number),
            'period': '700'
        },
    ],
    params_500 = [
        {
            'number': str(number) + '1',
            'period': 600
        },

        {
            'period': 700
        }
    ]
    for param in params_400:
        r = IVR.reserve_number(data['login'], data['password'], param)
        assert r.status_code == 400
    for param in params_500:
        r = IVR.reserve_number(data['login'], data['password'], param)
        assert r.status_code == 500


@pytest.mark.skip(reason='not available from NMS')
def test_check_period():
    number = IVR.get_random_number_for_reserve()
    params = {
        'number': number,
        'period': 10
    }
    r = IVR.reserve_number(data['login'], data['password'], params)
    assert r.status_code == 201
    response = r.json()
    assert 'reserved_uid' in response[0]
    reserved_uid = response[0]['reserved_uid']
    r = get_number_info(number)
    assert r['result'][0]['state_name'] == "RESERVED"
    time.sleep(params['period'])
    r = get_number_info(number)
    assert r['result'][0]['state_name'] == "FREE"
