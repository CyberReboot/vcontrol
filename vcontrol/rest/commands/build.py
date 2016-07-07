from ..helpers import get_allowed

import subprocess
import web

class BuildCommandR:
    """
    This endpoint is building Docker images on an machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        data = web.input()
        cmd = "/usr/local/bin/docker-machine ssh "+machine+" /bin/sh /data/build_images.sh"
        # !! TODO test with swagger
        if 'no_cache' in data:
            if not data['no_cache']:
                cmd += " --no-cache"
        try:
            out = subprocess.check_output(cmd, shell=True)
        except:
            return "failed to build"
        return "done building"
