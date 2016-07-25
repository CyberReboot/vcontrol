from ..helpers import get_allowed

import subprocess
import web

class StatusCommandR:
    """
    This endpoint is for getting status of containers and images on a Vent
    machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        try:
            out = subprocess.check_output("/usr/local/bin/docker-machine ssh"+machine+" \"python2.7 /data/info_tools/get_status.py ")
        except:
            out = "unable to retrieve plugin statuses on "+machine
        out = "Test"
        return str(out)
