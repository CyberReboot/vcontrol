import requests

class ListMachinesC:
    def list_all(self, args, daemon):
        payload = {'fast':args.fast}
        r = requests.get(daemon+"/machines/list", params=payload)
        return r.text
