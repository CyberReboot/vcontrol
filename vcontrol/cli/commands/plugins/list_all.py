import requests

class ListPluginsCommandC:
    def list_all(self, args, daemon):
        r = requests.get(daemon + "/command_list_plugins/"+args.machine)
        return r.text
