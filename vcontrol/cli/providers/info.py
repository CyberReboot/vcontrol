import requests

class InfoProviderC:
    def info(self, args, daemon):
        r = requests.get(daemon+"/get_info_providers/"+args.provider)
        return r.text
