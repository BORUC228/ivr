import requests
import json
import urllib3
from devconfig import setUpConfig

data = setUpConfig()

# Porta


def get_customer_info(customer_name):
    api_hostname = '172.16.102.19:443'
    api_user = 'EGoncharenko_126'
    api_password = 'FEBFEB99'

    # for self-signed certificates
    urllib3.disable_warnings()

    api_base = 'https://%s/rest/' % api_hostname

    # login
    req_data = {'params': json.dumps({'login': api_user, 'password':
        api_password})}
    r = requests.post(api_base + 'Session/login', data=req_data,
                      verify=False)
    data = r.json()
    session_id = data['session_id']
    print("Started session: %s" % session_id)

    # get currency list
    req_data = {'auth_info': json.dumps({'session_id': session_id}),
                'params': json.dumps({'name': customer_name})}
    r = requests.post(api_base + 'Customer/get_customer_info',
                      data=req_data, verify=False)
    assert r.status_code == 200
    return r.json()

# NMS


def get_number_info(number):
    url = data['nms_url']
    params = {
        'jsonrpc': '2.0',
        'method': 'scriptExecute',
        'params': {
            'projectName': 'NMS API',
            'reportName': 'getNumberInfo',
            'jsonOperParams': [
                {
                    'paramName': 'pNum_Code',
                    'paramValue': int(number)
                }
            ]
        },
        'id': "auto999"
    }
    r = requests.post(url, json=params)
    assert r.status_code == 200
    response = r.json()
    return response

