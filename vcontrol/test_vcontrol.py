from paste.fixture import TestApp

import vcontrol

import ast
import pkg_resources
import pytest
import web

def start_web_app():
    """ starts the web app in a TestApp for testing """
    vc_inst = vcontrol.VControl()
    urls = vc_inst.urls()
    app = web.application(urls, globals())
    testApp = TestApp(app.wsgifunc())
    return testApp

def test_index_r():
    """ tests the restful endpoint: index """
    # get web app
    testApp = start_web_app()

    # test index
    r = testApp.get('/v1')
    assert r.status == 200
    assert r.normal_body == "vcontrol"
    r = testApp.get('/v1/')
    assert r.status == 200
    assert r.normal_body == "vcontrol"

def test_version_r():
    """ tests the restful endpoint: version """
    # get web app
    testApp = start_web_app()

    # test version
    r = testApp.get('/v1/version')
    assert r.status == 200
    v = pkg_resources.get_distribution('vcontrol').version
    assert ast.literal_eval(r.normal_body)['version'] == v
