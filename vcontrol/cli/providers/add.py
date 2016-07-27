import json
import os
import requests

class AddProviderC:
    def add(self, provider, args, daemon):
        """
        only privileged can add providers, which currently is only
        accessible from the server running the vcontrol daemon
        """
        open_d = os.environ.get('VENT_CONTROL_OPEN')
        if open_d != "true":
            # daemon as passed in is: 'http:..../'+api_v
            # split and get the end and append
            api_v = daemon.split('/')[-1]
            daemon = 'http://localhost:8080/'+api_v
        if provider == "virtualbox":
            payload = {'name': args.name, 'provider': provider}
        else:
            payload = {'name': args.name, 'provider': provider, 'args': args.args}
        if provider == "openstack" or provider == "vmwarevsphere":
            payload['cpu'] = str(args.max_cpu_usage)
            payload['ram'] = str(args.max_ram_usage)
            payload['disk'] = str(args.max_disk_usage)
        r = requests.post(daemon+"/providers/add", data=json.dumps(payload))
        return r.text
