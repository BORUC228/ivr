import helperIVRKit as IVR
from devconfig import setUpConfig
from helperIVRKit import random_generator

data = setUpConfig()
bearer_token = IVR.take_token(data['login'], data['password'])
number_id = 102
scenario_id = 100


def test_create_route():
    # Получить список номеров, получить список сценариев, запросить  занятные роуты, которые уже созданы
    params = {
        "access_number": {
            "id": number_id
        },
        "destination_scenario": {
            "id": scenario_id
        },
    }
    r = IVR.create_route(bearer_token, data['customer_id'], params)
    assert r.status_code == 201
    response = r.json()
    assert response['id']
    assert params['access_number']['id'] == response['access_number']['id']
    assert params['destination_scenario']['id'] == response['destination_scenario']['id']


def test_invalid_customer_id():
    params = {
        "access_number": {
            "id": number_id
        },
        "destination_scenario": {
            "id": scenario_id
        },
    }
    r = IVR.create_route(bearer_token, '900000', params)
    assert r.status_code == 400
    r = IVR.create_route(bearer_token, 'dsa233', params)
    assert r.status_code == 400


def test_missing_required_params():
    params = [
        {
            "access_number": {
                "id": number_id
            }
        },
        {
            "destination_scenario": {
                "id": scenario_id
            }
        }
    ]
    for case in params:
        r = IVR.create_route(bearer_token, data['customer_id'], case)
        assert r.status_code == 400


def test_unique_params():
    params = {
        "access_number": {
            "id": number_id
        },
        "destination_scenario": {
            "id": scenario_id
        },
    }
    r = IVR.create_route(bearer_token, data['customer_id'], params)
    assert r.status_code == 201
    r = IVR.create_route(bearer_token, data['customer_id'], params)
    assert r.status_code == 400


def test_wrong_type_params():
    params = [
        {
            "access_number": {
                "id": str(number_id)
            },
            "destination_scenario": {
                "id": scenario_id
            }
        },
        {
            "access_number": {
                "id": number_id
            },
            "destination_scenario": {
                "id": str(scenario_id)
            }
        }
    ]
    for case in params:
        r = IVR.create_route(bearer_token, data['customer_id'], params)
        assert r.status_code == 400


def test_restricted_params():
    params = [
        {
            "access_number": {
                "id": 9999999999999
            },
            "destination_scenario": {
                "id": scenario_id
            }
        },
        {
            "access_number": {
                "id": number_id
            },
            "destination_scenario": {
                "id": 999999999999999
            }
        }
    ]
    for case in params:
        r = IVR.add_resource(data['login'], data['password'], id, case)
        assert r.status_code == 400


#def test_forbidden_params():
    # Сделать запрос под одним кастомером, под вторым кастомер, сохранить айдишники ресурсов, кросс запросы
