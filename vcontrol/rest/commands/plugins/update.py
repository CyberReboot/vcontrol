from ...helpers import get_allowed
import ast
import base64
import json
import os
import subprocess
import web

class UpdatePluginCommandR:
    """
    This endpoint is for updating an existing plugin repository on a Vent machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def OPTIONS(self):
        return self.POST()

    def POST(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        data = web.data()
        payload = {}
        try:
            payload = ast.literal_eval(data)
            if type(payload) != dict:
                payload = ast.literal_eval(json.loads(data))
        except:
            return "malformed json body"

        try:
            if "machine" in payload:
                if "url" in payload:
                    url = payload["url"]
                    if "user" and "pw" in payload:
                        user = payload["user"]
                        pw = payload["pw"]
                        cmd = "/usr/local/bin/docker-machine ssh "+payload["machine"]+" \"python2.7 /data/plugin_parser.py update_plugins "+url+" "+user+" "+pw+" private\""
                    else:
                        cmd = "/usr/local/bin/docker-machine ssh "+payload["machine"]+" \"python2.7 /data/plugin_parser.py update_plugins "+url+"\""
                    output = subprocess.check_output(cmd, shell=True)
                    if output == "":
                        output = "successfully updated "+url
                else:
                    output = "failed to update "+url+" -- no url specified"
            else:
                output = "failed to update "+url+" -- no machine specified"
        except Exception as e:
        	output = str(e)
        return output
