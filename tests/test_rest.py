from vcontrol.rest.commands import info

import requests

def test_info_command_r():
    """ tests the InfoCommandR class """
    r = requests.get('http://localhost:8080/v1/commands/info/foo')
    assert r.text == 'unable to get info on foo'
    c_inst = info.InfoCommandR()
    c_inst.GET("foo")
