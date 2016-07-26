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
            out = subprocess.check_output("/usr/local/bin/docker-machine ssh "+machine+" \"python2.7 /data/info_tools/get_status.py all\"", shell=True)
            output = ast.literal_eval(out)
            running = output['Running']
            nrunning = output['Not Running']
            built = output['Built']
            nbuilt = output['Not Built']
            disabled_containers = output['Disabled Containers']
            disabled_images = output['Disabled Images']
            errors = {key:output[key] for key in ['Running Errors', 'Not Running Errors', 'Built Errors']}

            if category == "all":
                out = str(output)
            elif category == "running_containers":
                out = str(running)
            elif category == "nr_containers":
                out = str(nrunning)
            elif category == "built_images":
                out = str(built)
            elif category == "nb_images":
                out = str(nbuilt)
            elif category == "disabled_containers":
                out = str(disabled_containers)
            elif category == "disabled_images":
                out = str(disabled_images)
            elif category == "errors":
                out = str(errors)
            else:
                out = "Invalid category for plugin status"
        except:
            out = "unable to retrieve plugin statuses on "+machine
        return str(out)
