import helperIVRKit as IVR
import pprint
import time
import json
import requests
import urllib3
import connectors
import random
from devconfig import setUpConfig
from connectors import get_number_info

data = setUpConfig()

number = IVR.get_random_number_for_reserve()
query = connectors.search_record_postgres('SELECT cmgtc.id,cmgtc.name from customer_mgt.customer as cmgtc '
                                          'LEFT JOIN customer_mgt.characteristic as cmc '
                                          'ON cmgtc.id = cmc.characteristic_customer_id '
                                          'WHERE cmgtc.status = %(status)s and cmc.name = \'billingId\'',
                                          {'status': 'active'})
random_record = random.choice(query)
id = random_record[0]
customer_name = random_record[1]
print(number)
print(id)
print(customer_name)

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
            'params': json.dumps({'id': '74951374043'})}
r = requests.post(api_base + 'Account/get_account_info',
                  data=req_data, verify=False)
assert r.status_code == 200
response = r.json()
pprint.pprint(response['account_info']['customer_name'])
