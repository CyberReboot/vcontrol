from ..helpers import get_allowed

import web

class BootMachineR:
    allow_origin, rest_url = get_allowed.get_allowed()
    def get(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # TODO
        return 1
