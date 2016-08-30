from ..helpers import get_allowed

import web

class InfoProviderR:
    """
    This endpoint is for getting info about a provider.
    """
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return "not implemented yet"
