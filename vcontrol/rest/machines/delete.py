from ..helpers import get_allowed

import os
import subprocess
import web

class DeleteMachineR:
    """
    This endpoint is for delete an existing machine of Vent.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        data = web.input()
        cmd = "/usr/local/bin/docker-machine rm -y"
        if 'force' in data:
            if data['force']:
                cmd += " -f"
        cmd += " "+machine
        try:
            out = subprocess.check_output(cmd, shell=True)
            if os.path.isfile('/root/.ssh/id_vent_generic_'+machine):
                os.remove('/root/.ssh/id_vent_generic_'+machine)
        except:
            out = "unable to delete machine"
        return str(out)
