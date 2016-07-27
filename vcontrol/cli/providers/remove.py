import os
import requests

class RemoveProviderC:
    def remove(self, args, daemon):
        """
        only privileged can remove providers, which currently is only
        accessible from the server running the vcontrol daemon
        """
        open_d = os.environ.get('VCONTROL_OPEN')
        if open_d != "true":
            # daemon as passed in is: 'http:..../'+api_v
            # split and get the end and append
            api_v = daemon.split('/')[-1]
            daemon = 'http://localhost:8080/'+api_v
        r = requests.get(daemon+"/providers/remove/"+args.provider)
        return r.text
