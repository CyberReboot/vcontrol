from ..helpers import get_allowed

import ast
import json
import os
import subprocess
import web

class DownloadCommandR:
    """
    This endpoint is for retrieving the template file of an machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def OPTIONS(self):
        return self.POST()
    def POST(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        web.header('Access-Control-Allow-Headers', "Content-type")
        # !! TODO does this work with swagger?
        data = web.data()
        payload = {}
        try:
            payload = ast.literal_eval(data)
            if type(payload) != dict:
                payload = ast.literal_eval(json.loads(data))
        except Exception as e:
            return "malformed json body", str(e)

        try:
            filedir = '/tmp/templates/'+payload['machine']
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            cmd = "docker-machine scp "+payload['machine']+":/var/lib/docker/data/templates/"+payload['template']+" "+filedir
            output = subprocess.check_output(cmd, shell=True)
            f = open(filedir+"/"+payload['template'], 'rb')
            return f.read()
        except Exception as e:
            return "failed to download", str(e)
        return "failed to download", str(e)
