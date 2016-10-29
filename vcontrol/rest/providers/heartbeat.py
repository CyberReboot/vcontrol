from ..helpers import get_allowed

import os
import web

class HeartbeatProvidersR:
    """
    This endpoint is just a quick way to ensure that providers are still
    reachable.
    """
    allow_origin, rest_url = get_allowed.get_allowed()
    def GET(self):
        web.header('Access-Control-Allow-Origin', self.allow_origin)
        providers = {}
        try:
            if os.path.isfile('providers.txt'):
                with open('providers.txt', 'r') as f:
                    for line in f:
                        try:
                            name, p_type, _, _, _, args = line.split(":", 5)
                            print(p_type)
                            if p_type in ["vmwarevsphere", "openstack"]:
                                if "--openstack-auth-url" in args:
                                    args = args.split("--openstack-auth-url ")[1]
                                    host_url = args.split(" ")[0]
                                    host = host_url.split("/")[2].split(":")[0]
                                    response = os.system("ping -W1 -c 1 " + host + "> /dev/null")
                                    if response == 0:
                                        providers[name] = "healthy"
                                    else:
                                        providers[name] = "unable to ping provider"
                                elif "--vmwarevsphere-vcenter" in args:
                                    args = args.split("--vmwarevsphere-vcenter ")[1]
                                    host = args.split(" ")[0]
                                    response = os.system("ping -W1 -c 1 " + host + "> /dev/null")
                                    if response == 0:
                                        providers[name] = "healthy"
                                    else:
                                        providers[name] = "unable to ping provider"
                                else:
                                    providers[name] = "unable to get connection information for provider"
                            else:
                                providers[name] = "heartbeat feature not available for this provider type"
                        except Exception as e:
                            providers[line.split(":", 1)[0]] = "heartbeat feature not available for this provider type"
        except Exception as e:
            return "unable to heartbeat providers", str(e)
        return str(providers)
