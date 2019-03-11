import requests
from support.assertions import assert_valid_schema


def test_get_user():
    # Do whatever is necessary to create a user here…

    headers = {'Content-Type': 'application/json'}
    base_url = 'http://172.16.102.95:8095/resourceOrderingManagement/resource//filters/71'
    r = requests.get(base_url, headers=headers)
    response = r.json()
    assert_valid_schema(response, 'getResource.json')
