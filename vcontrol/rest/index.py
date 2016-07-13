from helpers import get_allowed

import web

class IndexR:
    """
    This endpoint is just a quick way to ensure that the vcontrol API is up and
    running properly
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self):
        """ GET HTTP Request """
        web.header("Content-Type","text/plain")
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        return "vcontrol"
