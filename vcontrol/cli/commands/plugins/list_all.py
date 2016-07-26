import requests

class ListPluginsCommandC:
    def list_all(self, args, daemon):
        r = requests.get(daemon + "/commands/plugins/list/"+args.machine)
        return r.text
