import requests
import helperIVRKit as IVR
import connectors
from devconfig import setUpConfig

data = setUpConfig()
scenarios_types = ['VoiceState', 'HttpState', 'OutgoingCallState', 'SqlState', 'RouteState', 'ReleaseCallState',
                   'ScriptState', 'CallBackState', 'HttpWaitRequestState', 'HttpResponseState', 'CgPN_FilterState',
                   'ScheduleFilterState']


def test_get_all_scenarios_templates():
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_templates_scenario(bearer_token)
    assert r.status_code == 200
    response = r.json()
    found_scenarios = []
    for schema in response:
        if schema['Name'] in scenarios_types:
            found_scenarios.append(schema['Name'])
    assert scenarios_types == found_scenarios
    assert len(scenarios_types) == len(found_scenarios)


def test_get_scenario_with_filters():
    bearer_token = IVR.take_token(data['login'], data['password'])
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    for scenario in scenarios_types:
        base_url = data['ivr_url'] + '/state-templates?name=' + scenario
        r = requests.get(base_url, headers=headers)
        assert r.status_code == 200
        response = r.json()
        assert len(response) == 1
        assert response[0]['Name'] == scenario


def test_wrong_filters():
    bearer_token = IVR.take_token(data['login'], data['password'])
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + bearer_token}
    base_url = data['ivr_url'] + '/state-templates?name=limonad'
    r = requests.get(base_url, headers=headers)
    assert r.status_code == 200
    response = r.json()
    assert response is None
