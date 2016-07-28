from ..helpers import get_allowed

import web

class StatsProviderR:
    """
    This endpoint is for getting stats about a provider.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return "not implemented yet"
