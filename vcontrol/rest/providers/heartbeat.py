from ..helpers import get_allowed

import web

class HeartbeatProvidersR:
    """
    This endpoint is just a quick way to ensure that providers are still
    reachable.
    """
    def GET(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return 1
