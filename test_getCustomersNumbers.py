import helperIVRKit as IVR
import connectors
from devconfig import setUpConfig

data = setUpConfig()


# valid create - 200
def test_customer_with_numbers():
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_customer_numbers(bearer_token, 10777)
    assert r.status_code == 200
    response = r.json()
    assert response is not None


def test_customer_without_numbers():
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_customer_numbers(bearer_token, 10772)
    assert r.status_code == 200
    response = r.json()
    assert response is None

'''
Нет валидации на существование кастомера
def test_not_existing_customer():
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_customer_numbers(bearer_token, 999999)
    assert r.status_code == 404
    response = r.json()
    assert response is None
'''


'''
Вопрос об обработке запроса
def test_customer_with_invalid_id():
    bearer_token = IVR.take_token(data['login'], data['password'])
    r = IVR.get_customer_numbers(bearer_token, 'ballon')
    assert r.status_code == 200
    response = r.json()
    assert response is None
'''
