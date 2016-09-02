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
        file_path = None

        # get version number
        try:
            import pkg_resources
            version['version'] = pkg_resources.get_distribution('vcontrol').version
        except:
            pass

        # only allowed if in the git directory
        if not version:
            # get commit id
            try:
                cmd = 'git -C ../vcontrol rev-parse HEAD'
                commit_id = subprocess.check_output(cmd, shell=True)
                cmd = 'git -C ../vcontrol diff-index --quiet HEAD --'
                dirty = subprocess.call(cmd, shell=True)
                if dirty != 0:
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
