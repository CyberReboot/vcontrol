from ..helpers import get_allowed

import ast
import subprocess
import web
import sys

class MimetypesCommandR:
    """
    This endpoint is for getting the mimetypes and installed namespace on
    a Vent machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine, command):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        try:
            out = ""
            output = None
            # get all mimetypes supported by this vent instance
            if command == "mimetypes":
                out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"python2.7 /data/info_tools/get_namespaces.py -m\"", shell=True)
                output = ast.literal_eval(out)
                output = {'mimetypes': output}
        except:
            print(sys.exc_info())
            output = "Invalid command: "+command+" for retrieving mimetypes on "+machine
        return str(output)
