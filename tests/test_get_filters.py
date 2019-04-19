from tests import helperIVRKit as IVR
from tests.devconfig import setUpConfig

data = setUpConfig()

'''
Возможно нужно проверять ключи в массивах (элементы фильтрации)
'''


def test_get_all_filters():
    r = IVR.get_filter(data['login'], data['password'])
    assert r.status_code == 200
    response = r.json()
    assert response != []
