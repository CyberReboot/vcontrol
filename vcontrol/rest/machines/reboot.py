from ..helpers import get_allowed

import subprocess
import web

class RebootMachineR:
    """
    This endpoint is for rebooting a running machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        try:
            out = subprocess.check_output("/usr/local/bin/docker-machine restart "+machine, shell=True)
        except:
            out = "unable to reboot machine"
        return str(out)
