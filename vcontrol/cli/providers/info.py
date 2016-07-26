import requests

class InfoProviderC:
    def info(self, args, daemon):
        r = requests.get(daemon+"/providers/info/"+args.provider)
        return r.text
