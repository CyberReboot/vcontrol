from ..helpers import get_allowed

import subprocess
import web

class DeleteMachineR:
    """
    This endpoint is for delete an existing machine of Vent.
    """
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        data = web.input()
        cmd = "/usr/local/bin/docker-machine rm"
        if 'force' in data:
            if data['force']:
                cmd += " -f"
        cmd += " "+machine
        try:
            out = subprocess.check_output(cmd, shell=True)
        except:
            out = "unable to delete machine"
        return str(out)
