from ..helpers import get_allowed

import web

class InfoCommandR:
    """
    This endpoint is for getting info about a Vent machine.
    """
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return 1
