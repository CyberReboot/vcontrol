from ..helpers import get_allowed

import web

class SSHMachineR:
    """
    This endpoint is for SSHing into a Vent machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return "not implemented yet"
