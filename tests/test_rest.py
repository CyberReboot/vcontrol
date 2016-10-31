from vcontrol.rest.commands import info
from vcontrol.rest.commands.plugins import add

import requests

def test_info_command_r():
    """ tests the InfoCommandR class """
    r = requests.get('http://localhost:8080/v1/commands/info/foo')
    assert r.text == 'unable to get info on foo'
    c_inst = info.InfoCommandR()
    c_inst.GET("foo")

def test_plugin_add_command():
    """ tests rest/commands/plugin/add """
    data = {'broken': 'broken'}
    r = requests.post('http://localhost:8080/v1/commands/plugin/add', data=data)
    assert 'no machine specified' in r.text
