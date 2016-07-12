from ..helpers import get_allowed

import web

class HeartbeatMachinesR:
    """
    This endpoint is just a quick way to ensure that Vent machines are still
    reachable.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return 1
