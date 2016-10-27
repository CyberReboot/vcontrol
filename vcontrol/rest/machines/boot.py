from ..helpers import get_allowed

import subprocess
import web

class BootMachineR:
    """
    This endpoint is for booting a stopped machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        try:
            web.header('Access-Control-Allow-Origin', self.allow_origin)
        except Exception as e:
            print(e.message)
        try:
            out = subprocess.check_output("/usr/local/bin/docker-machine start "+machine, shell=True)
        except:
            out = "unable to start machine"
        return str(out)
