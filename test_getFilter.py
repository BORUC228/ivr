import helperIVRKit as IVR


def test_get_all_filters():
    r = IVR.get_filter('Creep', 'Walk')
    assert r.status_code == 200
    response = r.json()
    assert response != []
