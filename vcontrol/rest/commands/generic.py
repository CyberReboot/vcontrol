from ..helpers import get_allowed

import ast
import json
import subprocess
import web

class GenericCommandR:
    """
    This endpoint is for running an arbitrary command on an machine and getting
    the result back.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def OPTIONS(self, machine):
        return self.POST(machine)

    def POST(self, machine):
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
            command = payload['command']
        except:
            out = "you must specify a command"
            return out
        try:
            cmd = "/usr/local/bin/docker-machine ssh "+machine+" \""+command+"\""
            out = subprocess.check_output(cmd, shell=True)
        except:
            out = "unable to execute generic command"
        return str(out)
