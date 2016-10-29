from ..helpers import get_allowed

import os
import subprocess
import sys
import web

class ListMachinesR:
    """
    This endpoint lists all of the machines that have been created or registered.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        data = web.input()
        machine_array = []
        try:
            if 'fast' in data and data['fast'] == 'True':
                # !! TODO parse out the config.json file for the label
                # !! TODO use current users home directory instead of /root
                if os.path.isdir('/root/.docker/machine/machines'):
                    out = subprocess.check_output("ls -1 /root/.docker/machine/machines", shell=True)
                    out = str(out)
                    out = out.split("\n")
                    for machine in out[:-1]:
                        machine_array.append(machine)
                else:
                    out = ""
            else:
                out = subprocess.check_output("/usr/local/bin/docker-machine ls --filter label=vcontrol_managed=yes", shell=True)
                out = str(out)
                out = out.split("\n")
                for machine in out[1:-1]:
                    i = machine.split(" ")
                    machine_array.append(i[0])
        except:
            print(sys.exc_info())
        return str(machine_array)
