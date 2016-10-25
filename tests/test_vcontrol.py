from vcontrol import vcontrol

import ast
import pkg_resources
import pytest
import requests
import web

def start_web_app():
    """ starts the web app in a TestApp for testing """
    vc_inst = vcontrol.VControl()
    urls = vc_inst.urls()
    app = web.application(urls, globals())
    return app

def test_index_r():
    """ tests the restful endpoint: index """
    # get web app
    test_app = start_web_app()
    host = "http://localhost:8080"

    # test index
    r = requests.get(host+'/v1')
    assert r.status_code == 200
    assert r.text == "vcontrol"
    r = requests.get(host+'/v1/')
    assert r.status_code == 200
    assert r.text == "vcontrol"

def test_version_r():
    """ tests the restful endpoint: version """
    # get web app
    test_app = start_web_app()
    host = "http://localhost:8080"

    # test version
    r = requests.get(host+'/v1/version')
    assert r.status_code == 200
    v = pkg_resources.get_distribution('vcontrol').version
    assert ast.literal_eval(r.text)['version'] == v
