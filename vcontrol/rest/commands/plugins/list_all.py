from ...helpers import get_allowed

import subprocess
import web

class ListPluginsCommandR:
    """
    This endpoint is for listing plugins installed on a Vent machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        out = ""
        try:
            out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"python2.7 /data/info_tools/get_status.py repos\"", shell=True)   
        except:
            out = "unable to get installed plugins of "+machine
        return str(out)
