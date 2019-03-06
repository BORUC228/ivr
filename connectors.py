import requests
import json
import urllib3
import psycopg2
import psycopg2.extras
from devconfig import setUpConfig



data = setUpConfig()

# Porta


def get_customer_info(customer_name):
    api_hostname = '172.16.102.19:443'
    api_user = 'EGoncharenko_126'
    api_password = 'march9999'

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


# CMAPI


def search_record_postgres(query, part):
    conn = psycopg2.connect(dbname=data['postgres']['dbname'], user=data['postgres']['user'],
                            password=data['postgres']['password'], host=data['postgres']['host'])
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, part)
    record = cursor.fetchmany(size=10)
    cursor.close()
    conn.close()
    return record

