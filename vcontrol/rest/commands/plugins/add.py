from ...helpers import get_allowed

import web

class AddPluginCommandR:
    """
    This endpoint is for adding a new plugin repository on a Vent machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine, url):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return 1
