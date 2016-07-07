from helpers import get_allowed

import web

class VersionR:
    """
    This endpoint is for returning the current running version of vcontrol
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self):
        """ GET HTTP Request """
        web.header("Content-Type","text/plain")
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        try:
            with open('VERSION', 'r') as f: v = f.read().strip()
        except:
            with open('../VERSION', 'r') as f: v = f.read().strip()
        return v
