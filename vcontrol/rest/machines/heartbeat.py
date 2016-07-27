from ..helpers import get_allowed

import subprocess
import web

class HeartbeatMachinesR:
    """
    This endpoint is just a quick way to ensure that Vent machines are still
    reachable.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self):
        out = ""
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        cmd = "docker-machine ls --filter label=vcontrol_managed=yes"
        try:
            out = subprocess.check_output(cmd, shell=True)
        except Exception as e:
            return "unable to heartbeat machines", str(e)
        return str(out)
