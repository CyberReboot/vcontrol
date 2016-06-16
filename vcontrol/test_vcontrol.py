from paste.fixture import TestApp

from vcontrol import *

import pytest
import web

def test_get_urls():
    a = get_urls()

def test_web():
    urls = get_urls()
    assert type(urls) == type(())
    app = web.application(urls, globals())
    testApp = TestApp(app.wsgifunc())

    # test index
    r = testApp.get('/v1')
    assert r.status == 200
    assert r.normal_body == "vcontrol"
    r = testApp.get('/v1/')
    assert r.status == 200
    assert r.normal_body == "vcontrol"

    # test version
    r = testApp.get('/v1/version')
    assert r.status == 200
    with open('VERSION', 'r') as f: v = f.read().strip()
    assert r.normal_body == v
