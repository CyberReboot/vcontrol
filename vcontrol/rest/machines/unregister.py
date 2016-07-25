from ..helpers import get_allowed

import os
import subprocess
import web

class UnregisterMachineR:
    """
    This endpoint is for unregistering an machine from vcontrol.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        try:
            out = subprocess.check_output("/usr/local/bin/docker-machine rm -y "+machine, shell=True)
            if os.path.isfile('/root/.ssh/id_vent_generic_'+machine):
                os.remove('/root/.ssh/id_vent_generic_'+machine)
        except Exception as e:
            out = "unable to unregister machine"
        return str(out)
