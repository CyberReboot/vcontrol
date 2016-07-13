import requests

class DeleteMachineC:
    def delete(self, args, daemon):
        """
        check if controlled by docker-machine, if not fail
        first ssh into the machine running vcontrol daemon
        from there use docker-machine to delete
        """
        payload = {'force':args.force}
        r = requests.get(daemon+"/delete_machine/"+args.machine, params=payload)
        return r.text
