from ..helpers import get_allowed

import ast
import json
import os
import web

class AddProviderR:
    """
    This endpoint allows for a new provider such as openstack or vmware to be added.
    A Vent machine runs on a provider. Note that a provider can only be added from localhost
    of the machine running vcontrol unless the environment variable VCONTROL_OPEN=true is set on the server.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def OPTIONS(self):
        return self.POST()

    def POST(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        web.header('Access-Control-Allow-Headers', "Content-type")
        open_d = os.environ.get('VCONTROL_OPEN')
        # TODO is this sufficient? probably not...
        if web.ctx.env["HTTP_HOST"] == 'localhost:8080' or open_d == "true":
            data = web.data()
            payload = {}
            try:
                payload = ast.literal_eval(data)
                if type(payload) != dict:
                    payload = ast.literal_eval(json.loads(data))
            except:
                return "malformed json body"

            try:
                if os.path.isfile('providers.txt'):
                    with open('providers.txt', 'r') as f:
                        for line in f:
                            if line.split(":")[0] == payload['name']:
                                return "provider already exists"
                # only get here if it didn't already return
                with open('providers.txt', 'a') as f:
                    if payload['provider'] == 'openstack' or payload['provider'] == 'vmwarevsphere':
                        f.write(payload['name']+':'+payload['provider']+':'+str(payload['cpu'])+":"+str(payload['ram'])+":"+str(payload['disk'])+":"+str(payload['args'])+'\n')
                    elif payload['provider'] == 'virtualbox':
                        f.write(payload['name']+':'+payload['provider']+'\n')
                    else:
                        f.write(payload['name']+':'+payload['provider']+':'+str(payload['args'])+'\n')
                return "successfully added provider"
            except:
                return "unable to add provider"
        else:
            return "must be done from the localhost running vcontrol daemon"
