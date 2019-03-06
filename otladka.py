import helperIVRKit as IVR
import pprint
import time
import connectors
import random
from devconfig import setUpConfig
from connectors import get_number_info

data = setUpConfig()

# number = IVR.get_random_number_for_reserve()
# r = connectors.search_record_postgres('SELECT * FROM customer_mgt.customer_mgt.customer WHERE name = %(name)s',
#                                       {'name': 'VAVAVAV'})
# print(r[0][4])

number = IVR.get_random_number_for_reserve()
params = {
    'number': str(number),
    'period': 600
}
pprint.pprint(params)
r = IVR.reserve_number(data['login'], data['password'], params)
pprint.pprint(r)
assert r.status_code == 201
response = r.json()
pprint.pprint(response)
# assert 'reserved_uid' in response[0]
# reserved_uid = response[0]['reserved_uid']
# r = get_number_info(number)
# assert r['result'][0]['state_name'] == "RESERVED"
# delete_params = {
#     'number': number,
#     'reserved_uid': reserved_uid
# }
# r = IVR.delete_reserved_number(data['login'], data['password'], delete_params)
# assert r.status_code == 204
# r = get_number_info(number)
# assert r['result'][0]['state_name'] == "FREE"