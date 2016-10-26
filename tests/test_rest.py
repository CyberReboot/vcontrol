from vcontrol.rest.commands import info
# from vcontrol.rest.providers import list_all

import requests

def test_info_command_r():
    """ tests the InfoCommandR class """
    r = requests.get('http://localhost:8080/v1/commands/info/foo')
    assert r.text == 'unable to get info on foo'
    c_inst = info.InfoCommandR()
    c_inst.GET("foo")



def test_providers_list_all():
    """ tests the ListProvidersR class """
    r = requests.get('http://localhost:8080/v1/providers/list')
    assert r.status_code == 200
    assert r.json() == {}