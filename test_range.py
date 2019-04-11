import helperIVRKit as IVR
from devconfig import setUpConfig


data = setUpConfig()
customer_id = data['customer_id']


def test_range():
    function_with_range = ['get_customer_scenarios', 'get_customers', 'get_customer_numbers', 'get_customer_routes',
                           'get_customer_voice_messages']
    for function in function_with_range:
        base_url = ''
        if function == 'get_customers':
            base_url = data['ivr_url'] + '/customers'
        if function == 'get_customer_scenarios':
            base_url = data['ivr_url'] + '/customers/'+customer_id+'/scenarios'
        if function == 'get_customer_numbers':
            base_url = data['ivr_url'] + '/customers/'+customer_id+'/numbers'
        if function == 'get_customer_routes':
            base_url = data['ivr_url'] + '/customers/'+customer_id+'/routes'
        if function == 'get_customer_voice_messages':
            base_url = data['ivr_url'] + '/customers/'+customer_id+'/voice_messages'
        range_word = base_url.split('/')
        range_unit = range_word[-1]
        ranges = [range_unit+'=10-1',
                  range_unit+'=0-99',
                  range_unit+'=2-2',
                  range_unit+'=1-',
                  range_unit+'=-3',
                  range_unit+'=1-l',
                  range_unit+'s=0-99']
        r = IVR.get_ranges(base_url, ranges[0])
        assert r.status_code == 416
        r = IVR.get_ranges(base_url, ranges[1])
        assert r.status_code == 206
        response = r.json()
        assert 0 <= len(response) <= 100
        r = IVR.get_ranges(base_url, ranges[2])
        assert r.status_code == 206
        response = r.json()
        assert 0 <= len(response) <= 1
        r = IVR.get_ranges(base_url, ranges[3])
        assert r.status_code == 206
        response = r.json()
        assert 0 <= len(response) <= 10
        r = IVR.get_ranges(base_url, ranges[4])
        assert r.status_code == 416
        r = IVR.get_ranges(base_url, ranges[5])
        assert r.status_code == 416
        r = IVR.get_ranges(base_url, ranges[6])
        assert r.status_code == 206
        response = r.json()
        assert 0 <= len(response) <= 10
