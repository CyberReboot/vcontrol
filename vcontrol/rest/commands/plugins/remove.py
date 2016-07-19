from ...helpers import get_allowed
import ast
import json
import subprocess
import web

class RemovePluginCommandR:
    """
    This endpoint is for removing a new plugin repository on a Vent machine.
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
                    cmd = "/usr/local/bin/docker-machine ssh "+payload["machine"]+" \"python2.7 /data/plugin_parser.py remove_plugins "+url+"\""
                    output = subprocess.check_output(cmd, shell=True)
                    if output == "":
                        output = "successfully removed "+url
                else:
                    output = "failed to remove plugin -- no url specified"
            else:
                output = "failed to remove plugin -- no machine specified"
        except Exception as e:
        	output = str(e)
        return output
