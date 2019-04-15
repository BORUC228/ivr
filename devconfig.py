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
        'customer_id': '10848',
        'scenario_id': '321',
        "States": [
            {
                "Type": "OutgoingCallState",
                "Name": "Состояние 1",
                "Comment": "",
                "ArgList": [],
                "x": 596,
                "y": 290,
                "Root": True,
                "CallBacks": {
                    "OnSuccess": {
                        "Type": "FinishAction"
                    }
                },
                "SendAnswer": False,
                "CgPN": {
                    "Type": "Const",
                    "Value": "797700000"
                },
                "CdPN": {
                    "Type": "Const",
                    "Value": "791200000"
                },
                "MultiChannel": False,
                "CommonParams": {
                    "AcceptCallDTMF": "",
                    "DenyCallDTMF": "",
                    "RdPN": {
                        "Type": "Const",
                        "Value": "79775633333"
                    },
                    "AdditionalCallHeaders": {}
                },
                "PlayAlertingFromB": False,
                "CallMode": "MC"
            }
        ],
    }
    return data
