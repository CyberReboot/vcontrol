import requests

class MimetypesCommandC:
    def retrieve(self, args, daemon):
        r = requests.get(daemon+"/commands/mimetypes/"+args.machine+"/"+args.command)
        return r.text
