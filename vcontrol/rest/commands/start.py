from ..helpers import get_allowed

import subprocess
import web

class StartCommandR:
    """
    This endpoint is for starting a specified category of containers on a
    specific machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine, category):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # just in case, make sure Vent-management is running first
        out = ""
        try:
            out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"python2.7 /data/template_parser.py "+category+" start\"", shell=True)
        except:
            out = "unable to start "+category+" on "+machine
        return str(out)
