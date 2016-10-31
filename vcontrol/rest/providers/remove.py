from ..helpers import get_allowed

import os
import web

class RemoveProviderR:
    """
    This endpoint allows for removing a provider such as openstack or vmware.
    A Vent machine runs on a provider, this will not remove existing Vent
    machines on the specified provider. Note that a provider can only be
    removed from localhost of the machine running vcontrol unless the
    environment variable VCONTROL_OPEN=true is set on the server.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self, provider):
        try:
            web.header('Access-Control-Allow-Origin', self.allow_origin)
        except Exception as e:
            print(e.message)
        open_d = os.environ.get('VCONTROL_OPEN')
        providers_file_path = os.path.join(os.path.dirname(__file__), 'providers.txt')
        if web.ctx.env["HTTP_HOST"] == 'localhost:8080' or open_d == "true":
            f = open(providers_file_path,"r")
            lines = f.readlines()
            f.close()
            flag = 0
            with open(providers_file_path, 'w') as f:
                for line in lines:
                    if not line.startswith(provider+":"):
                        f.write(line)
                    else:
                        flag = 1
            if flag:
                return "removed " + provider
            else:
                return provider + " not found, couldn't remove"
        else:
            return "must be done from the localhost running vcontrol daemon"
