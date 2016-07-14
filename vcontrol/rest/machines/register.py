from ..helpers import get_allowed

import ast
import json
import subprocess
import web

class RegisterMachineR:
    """
    This endpoint is for registering an existing Vent machine into vcontrol.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def OPTIONS(self):
        return self.POST()

    def POST(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        # generic driver
        data = web.data()
        payload = {}
        try:
            payload = ast.literal_eval(data)
            if type(payload) != dict:
                payload = ast.literal_eval(json.loads(data))
        except:
            return "malformed json body"

        try:
            # generate ssh keys
            out = subprocess.check_output('ssh-keygen -t rsa -b 4096 -C "vent-generic-'+payload['machine']+'" -f /root/.ssh/id_vent_generic_'+payload['machine']+' -q -N ""', shell=True)

            # upload public key
            out = subprocess.check_output('sshpass -p "'+payload['password']+'" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -q /root/.ssh/id_vent_generic_'+payload['machine']+'.pub docker@'+payload['ip']+':/tmp/', shell=True)
            out = subprocess.check_output('sshpass -p "'+payload['password']+'" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -q docker@'+payload['ip']+' "cat /tmp/id_vent_generic_'+payload['machine']+'.pub >> /home/docker/.ssh/authorized_keys && rm /tmp/id_vent_generic_'+payload['machine']+'.pub"', shell=True)

            # add to docker-machine
            out = subprocess.check_output('docker-machine create -d generic --generic-ip-address "'+payload['ip']+'" --generic-ssh-key "/root/.ssh/id_vent_generic_'+payload['machine']+'" --generic-ssh-user "docker" --engine-label vcontrol_managed=yes '+payload['machine'], shell=True)
        except Exception as e:
            out = "unable to register machine"
        return str(out)
