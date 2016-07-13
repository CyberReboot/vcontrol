from ..helpers import get_allowed

import web

class LogsCommandR:
    """
    This endpoint is for retrieving machine logs.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return 1
