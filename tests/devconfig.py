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
        'States': [
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
        'States_4_update': [
            {
                "Type": "VoiceState",
                "immediateSTT": True,
                "Name": "Hello",
                "ArgList": [],
                "x": 401,
                "y": 121,
                "Root": True,
                "CallBacks": {},
                "SendAnswer": True,
                "Announcement": [
                    {
                        "Message": {
                            "Type": "Const",
                            "Value": "tts=\"Добрый день! Скажите текст для отправки в смс\""
                        }
                    }
                ],
                "Prompt": [],
                "RepeatCount": {
                    "Type": "Const",
                    "Value": "1"
                },
                "InitialInputInterval": 10,
                "ItemList": [
                    {
                        "Prompt": [],
                        "DTMF": "1",
                        "Action": {
                            "Type": "TransitionAction",
                            "NewState": "SendSMS",
                            "ArgList": []
                        }
                    },
                    {
                        "Prompt": [],
                        "DTMF": "2",
                        "Action": {
                            "Type": "TransitionAction",
                            "NewState": "Состояние 3",
                            "ArgList": []
                        }
                    }
                ],
                "MVCInRow": False,
                "DelayedUserInput": False,
                "IsImmediateSTT": True
            },
            {
                "Type": "HttpState",
                "Name": "SendSMS",
                "ArgList": [],
                "x": 606,
                "y": 256,
                "Root": False,
                "CallBacks": {
                    "OnSuccess": {
                        "Type": "TransitionAction",
                        "NewState": "Состояние 5",
                        "ArgList": []
                    },
                    "OnError": {
                        "Type": "PrevStateTransitionAction"
                    }
                },
                "HttpRequest": {
                    "Host": {
                        "Type": "Const",
                        "Value": "172.16.102.138"
                    },
                    "Port": {
                        "Type": "Const",
                        "Value": "8080"
                    },
                    "ContentType": "application/json",
                    "Url": {
                        "Type": "Const",
                        "Value": "/v2/accounts/acc08eb1d65-52f9-40d5-a9a1-7368badb83f5/messages"
                    },
                    "Method": "POST",
                    "Body": {
                        "Type": "Script",
                        "Value": "\nreturn '{\"from\":\"79587625002\",\"to\":\"79775637968\",\"text\":\"' + ServiceContext.UserInput + '\",\"channel\":\"sms\"}';"
                    },
                    "Ssl": False,
                    "Headers": {
                        "Content-Type": {
                            "Type": "Const",
                            "Value": "application/json"
                        }
                    },
                    "AuthType": "BASIC",
                    "User": {
                        "Type": "Const",
                        "Value": "acc08eb1d65-52f9-40d5-a9a1-7368badb83f5"
                    },
                    "Pass": {
                        "Type": "Const",
                        "Value": "autc026f145-55bb-494e-90f6-aa4a65fc5fe4"
                    }
                },
                "RequestBuilder": ""
            },
            {
                "Type": "CgPN_FilterState",
                "Name": "Состояние 3",
                "ArgList": [],
                "x": 121,
                "y": 313,
                "Root": False,
                "CallBacks": {
                    "OnSuccess": {
                        "Type": "TransitionAction",
                        "NewState": "Состояние 9",
                        "ArgList": []
                    },
                    "OnError": {
                        "Type": "PrevStateTransitionAction"
                    }
                },
                "CgPN_Template": "79775660000"
            },
            {
                "Type": "HttpWaitRequestState",
                "Name": "Состояние 5",
                "ArgList": [
                    "у"
                ],
                "x": 15,
                "y": 502,
                "Root": False,
                "CallBacks": {
                    "OnTimeout": {
                        "Type": "FinishAction",
                        "ErrorCause": "Неудалось отправить сообщение"
                    },
                    "OnHttpRequest": {
                        "Type": "TransitionAction",
                        "NewState": "Состояние 1",
                        "ArgList": []
                    }
                },
                "TimeoutInterval": {
                    "Type": "Const",
                    "Value": "10"
                }
            },
            {
                "Type": "ScriptState",
                "Name": "Состояние 6",
                "ArgList": [],
                "x": 392,
                "y": 506,
                "Root": False,
                "Script": "return 'drop';",
                "AllowedTransitions": [
                    {
                        "NewState": "Hello",
                        "ArgList": []
                    },
                    {
                        "NewState": "Состояние 8",
                        "ArgList": []
                    }
                ]
            },
            {
                "Type": "CallBackState",
                "Name": "Состояние 8",
                "ArgList": [],
                "x": 405,
                "y": 868,
                "Root": False,
                "CallBacks": {
                    "OnSuccess": {
                        "Type": "FinishAction"
                    },
                    "OnError": {
                        "Type": "FinishAction",
                        "ErrorCause": "Беда"
                    }
                },
                "CgPN": {
                    "Type": "Const",
                    "Value": "88004561232"
                },
                "CdPN": {
                    "Type": "Const",
                    "Value": "79125550000"
                },
                "RdPN": {
                    "Type": "Const",
                    "Value": "7959262615"
                },
                "WAI": {
                    "Type": "Const",
                    "Value": "15"
                },
                "AdditionalCallHeaders": {
                    "Параметр_0": {
                        "Type": "Const",
                        "Value": "1"
                    }
                }
            },
            {
                "Type": "ScheduleFilterState",
                "Name": "Состояние 9",
                "ArgList": [],
                "x": 130,
                "y": 661,
                "Root": False,
                "CallBacks": {
                    "OnSuccess": {
                        "Type": "TransitionAction",
                        "NewState": "Состояние 8",
                        "ArgList": []
                    },
                    "OnError": {
                        "Type": "FinishAction",
                        "ErrorCause": "Не в диапазоне"
                    }
                },
                "Schedule": "schedule from 01/07/2018 to 30/04/2019 time [08:00:00-19:00:00] date 1..5 day 1,2,3 week 4 month 2019 year; time [00:00:00-23:59:59] date 6,7 day 3 week 4 month 2019 year;"
            },
            {
                "Type": "HttpResponseState",
                "Name": "Состояние 1",
                "ArgList": [
                    "heh i meh"
                ],
                "x": 615,
                "y": 670,
                "Root": False,
                "CallBacks": {
                    "OnSuccess": {
                        "Type": "TransitionAction",
                        "NewState": "Состояние 8",
                        "ArgList": []
                    }
                },
                "HttpResponse": {
                    "StatusCode": {
                        "Type": "Const",
                        "Value": "200"
                    },
                    "ContentType": "application/json",
                    "Body": {
                        "Type": "Const",
                        "Value": "{\"result\":\"ok\"}"
                    },
                    "Headers": {
                        "Range": {
                            "Type": "Const",
                            "Value": "numbers=100"
                        },
                        "Content-Type": {
                            "Type": "Const",
                            "Value": "x-ms-wma"
                        }
                    }
                }
            }
        ],
        'CommonScript': 'var x = 3'
    }
    return data
