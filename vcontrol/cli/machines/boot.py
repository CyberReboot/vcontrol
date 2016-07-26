import requests

class BootMachineC:
    def boot(self, args, daemon):
        """
        check if controlled by docker-machine, if not fail
        first ssh into the machine running vcontrol daemon
        from there use docker-machine to start
        """
        r = requests.get(daemon+"/machines/boot/"+args.machine)
        return r.text
