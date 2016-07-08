from ..helpers import get_allowed

import web

class CleanCommandR:
    """
    This endpoint is for cleaning all containers of a namespace on a Vent
    machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return 1
