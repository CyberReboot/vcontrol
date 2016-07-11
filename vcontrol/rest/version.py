from helpers import get_allowed

import json
import os
import subprocess
import web

class VersionR:
    """
    This endpoint is for returning the current running version of vcontrol
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self):
        """ GET HTTP Request """
        web.header("Content-Type","text/plain")
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        version = {}

        # get version number
        try:
            with open('VERSION', 'r') as f: version['version'] = f.read().strip()
        except:
            with open('../VERSION', 'r') as f: version['version'] = f.read().strip()

        # get commit id
        try:
            cmd = 'git -C ../vcontrol rev-parse HEAD'
            commit_id = subprocess.check_output(cmd, shell=True)
            cmd = 'git -C ../vcontrol diff-index --quiet HEAD --'
            dirty = subprocess.call(cmd, shell=True)
            if dirty != '0':
                version['commit'] = commit_id.strip() + '-dirty'
            else:
                version['commit'] = commit_id.strip()
        except:
            pass

        # get runtime id (docker container ID)
        try:
            if 'HOSTNAME' in os.environ:
                version['runtime'] = os.environ['HOSTNAME']
        except:
            pass

        return json.dumps(version)
