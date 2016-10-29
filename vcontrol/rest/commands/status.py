from ..helpers import get_allowed

import ast
import subprocess
import web
import sys

class StatusCommandR:
    """
    This endpoint is for getting status of containers and images on a Vent
    machine.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, machine, category):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        try:
            # get all plugin info
            out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"python2.7 /data/info_tools/get_status.py all\"", shell=True)
            output = ast.literal_eval(out)
            # break up into relevant information
            containers = {key:output[key] for key in ['Running', 'Not Running', 'Disabled Containers', 'Running Errors', 'Not Running Errors'] if key in output}
            images = {key:output[key] for key in ['Built', 'Not Built', 'Disabled Images', 'Built Errors'] if key in output}
            disabled = {key:output[key] for key in ['Disabled Containers', 'Disabled Images'] if key in output}
            errors = {key:output[key] for key in ['Running Errors', 'Not Running Errors', 'Built Errors'] if key in output}

            # return relevant information
            if category == "all":
                out = output
            elif category == "containers":
                out = containers
            elif category == "images":
                out = images
            elif category == "disabled":
                out = disabled
            elif category == "errors":
                out = errors
            else:
                # should never get here
                out = "Invalid category for plugin status"
        except:
            print(sys.exc_info())
            out = "unable to retrieve plugin statuses on "+machine
        return str(out)
