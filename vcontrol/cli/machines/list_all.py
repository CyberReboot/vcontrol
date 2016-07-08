import requests

class ListMachinesC:
    def list_all(self, args, daemon):
        payload = {'fast':args.fast}
        r = requests.get(daemon+"/list_machines", params=payload)
        return r.text
