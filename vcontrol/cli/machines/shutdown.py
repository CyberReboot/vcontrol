import requests

class ShutdownMachineC:
    def shutdown(self, args, daemon):
        """
        check if controlled by docker-machine, if not fail
        first ssh into the machine running vcontrol daemon
        from there use docker-machine to stop
        """
        r = requests.get(daemon+"/machines/shutdown/"+args.machine)
        return r.text
