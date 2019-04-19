from tests import helperIVRKit as IVR
import random
from tests.devconfig import setUpConfig

# category = ['REGULAR', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EXCLUSIVE']
# regionCode = ['RU', 'MOW', 'SPE', 'NIZ', 'TA', 'CHE', 'KGD', 'SVE', 'KDA', 'KYA', 'NVS', 'PER', 'ROS', 'SAM', 'TYU',
#               'VOR', 'KHM', 'OMS', 'TOM', 'KEM', 'ALT', 'CR', 'CR', 'CR', 'KDA', 'KIR', 'KEM', 'KRS', 'UD', 'BA',
#               'BEL', 'LIP', 'TVE', 'KLU', 'YAR', 'ORL', 'TUL', 'RYA', 'MUR', 'VGG', 'ARK', 'KOS', 'SAR', 'PRI', 'KHA',
#               'IVA', 'IRK', 'STA', 'KHM', 'CU', 'VLG', 'KHM', 'YAN', 'BEL', 'KDA', 'AST', 'ALT', 'YEV', 'AMU', 'BRY',
#               'VLA', 'VLG', 'IRK', 'KHA', 'CHE', 'DA', 'TA', 'SVE', 'KDA', 'ORE', 'ORE', 'PNZ', 'PSK', 'MO', 'SMO',
#               'SAM', 'KO', 'TAM', 'BU', 'ULY', 'ZAB', 'SAK', 'SAM', 'KGN']
# number_type = ['DEF', 'ABC', 'KDU', 'CEN', 'Local', 'National', 'TollFree', 'ITFS', 'UIFN']
mask = ['7495%']

data = setUpConfig()


def test_get_numbers_with_filter():
    bearer_token = IVR.take_token('Creep', 'Walk')
    start = 1
    end = 10
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token,
               'Range': 'numbers=' + str(start) + '-' + str(end)}
    i = 0
    numbers_found = False
    while i < 50:
        params = {
            'category': random.choice(data['category']),
            'owner': random.choice(data['owner']),
            'regionCode': random.choice(data['regionCode']),
            'type': random.choice(data['number_type']),
            # 'mask': random.choice(mask)
        }
        r = IVR.get_numbers(headers=headers, params=params)
        assert r.status_code == 206
        response = r.json()
        if response != []:
            assert len(response) <= (end - (start - 1))
            print(response)
            for element in response:
                assert element['owner'] == params['owner']
                assert element['category'] == params['category']
                assert element['regionCode'] == params['regionCode']
                assert element['type'] == params['type']
                assert element['state'] == 'FREE'
            numbers_found = True
            break
        else:
            print('Trying found: ' + params['category'] + ' ' + params['owner'] + ' ' + params['regionCode'] + ' ' +
                  params['type'])
            i += 1
    assert numbers_found is True


def test_get_numbers_with_missing_start_range():
    bearer_token = IVR.take_token('Creep', 'Walk')
    end = 15
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token,
               'Range': 'numbers=-' + str(end)}
    params = {
        'category': random.choice(data['category']),
        'owner': random.choice(data['owner']),
        'regionCode': random.choice(data['regionCode']),
        'type': random.choice(data['number_type']),
        # 'mask': random.choice(mask)
    }
    r = IVR.get_numbers(headers=headers, params=params)
    assert r.status_code == 416


def test_get_numbers_with_missing_end_range():
    bearer_token = IVR.take_token('Creep', 'Walk')
    start = 5
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token,
               'Range': 'numbers=' + str(start)}
    i = 0
    numbers_found = False
    while i < 50:
        params = {
            'category': random.choice(data['category']),
            'owner': random.choice(data['owner']),
            'regionCode': random.choice(data['regionCode']),
            'type': random.choice(data['number_type']),
            # 'mask': random.choice(mask)
        }
        r = IVR.get_numbers(headers=headers, params=params)
        assert r.status_code == 206
        response = r.json()
        if response != []:
            assert len(response) <= ((start + 10) - (start - 1))
            print(response)
            for element in response:
                assert element['owner'] == params['owner']
                assert element['category'] == params['category']
                assert element['regionCode'] == params['regionCode']
                assert element['type'] == params['type']
                assert element['state'] == 'FREE'
            numbers_found = True
            break
        else:
            print('Trying found: ' + params['category'] + ' ' + params['owner'] + ' ' + params['regionCode'] + ' ' +
                  params['type'])
            i += 1
    assert numbers_found is True


def test_numbers_without_filtering_number():
    bearer_token = IVR.take_token('Creep', 'Walk')
    start = 1
    end = 10
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token,
               'Range': 'numbers=' + str(start) + '-' + str(end)}
    r = IVR.get_numbers(headers=headers, params=None)
    assert r.status_code == 206
    response = r.json()
    assert len(response) > 0

