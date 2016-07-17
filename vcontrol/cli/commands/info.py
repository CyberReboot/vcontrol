import requests

class InfoCommandC:
    def info(self, args, daemon):
        r = requests.get(daemon+"/get_info_commands/"+args.machine)
        return r.text
