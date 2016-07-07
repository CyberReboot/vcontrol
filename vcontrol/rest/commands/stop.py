from ..helpers import get_allowed

import subprocess
import web

class StopCommandR:
    """
    This endpoint is for stopping a specified category of containers on a
    specific machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine, category):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        try:
            out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"python2.7 /data/template_parser.py "+category+" stop\"", shell=True)
        except:
            out = "unable to stop "+category+" on "+machine
        return str(out)
