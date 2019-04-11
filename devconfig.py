def setUpConfig():
    data = {
        'login': 'borucTheTest',
        'password': 'march9999',
        'bad_login': 'Kizaru',
        'ivr_url': 'http://172.16.102.95:8085/v1',
        'postgres': {
            'dbname': 'customer_mgt',
            'user': 'postgres',
            'password': 'postgres',
            'host': '172.16.102.96'
        },
        'category': ['REGULAR', 'BRONZE', 'SILVER'],
        'owner': ['MTT'],
        'regionCode': ['MOW'],
        'number_type': ['ABC'],
        'nms_url': 'http://172.16.122.30:8080/MTT.Reporter/webresources/API/json',
        'porta_url': '172.16.102.19:443',
        'customer_id': '10847',
        'scenario_id': '321',
    }
    return data
