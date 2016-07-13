from ..helpers import get_allowed

import subprocess
import web

class ShutdownMachineR:
    """
    This endpoint is for shutting down a running machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        try:
            out = subprocess.check_output("/usr/local/bin/docker-machine stop "+machine, shell=True)
        except:
            out = "unable to stop machine"
        return str(out)
