from ..helpers import get_allowed

import subprocess
import web

class InfoCommandR:
    """
    This endpoint is for getting info about a Vent machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        try:
            web.header('Access-Control-Allow-Origin', self.allow_origin)
        except Exception as e: # no pragma
            pass
        out = ""
        try:
            out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"/data/info_tools/get_info.sh all -v\"", shell=True)
        except:
            out = "unable to get info on "+machine
        return str(out)
