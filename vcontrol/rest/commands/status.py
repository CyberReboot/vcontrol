from ..helpers import get_allowed

import ast
import subprocess
import web

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
            running = output['Running']
            nrunning = output['Not Running']
            built = output['Built']
            nbuilt = output['Not Built']
            disabled_containers = output['Disabled Containers']
            disabled_images = output['Disabled Images']
            errors = {key:output[key] for key in ['Running Errors', 'Not Running Errors', 'Built Errors']}

            # return relevant information
            if category == "all":
                out = output
            elif category == "running_containers":
                out = running
            elif category == "nr_containers":
                out = nrunning
            elif category == "built_images":
                out = built
            elif category == "nb_images":
                out = nbuilt
            elif category == "disabled_containers":
                out = disabled_containers
            elif category == "disabled_images":
                out = disabled_images
            elif category == "errors":
                out = errors
            else:
                # should never get here
                out = "Invalid category for plugin status"
        except:
            out = "unable to retrieve plugin statuses on "+machine
        return str(out)
