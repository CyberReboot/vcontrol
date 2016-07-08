from ..helpers import get_allowed

import web

class StatusCommandR:
    """
    This endpoint is for getting status of containers and images on a Vent
    machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return 1
