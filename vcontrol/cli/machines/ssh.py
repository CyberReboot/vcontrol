import requests

class SSHMachineC:
    def ssh(self, args, daemon):
        """
        get the certs from the machine running vcontrol daemon
        from there ssh to the machine, whether with docker-machine or ssh
        """
        # docker exec into vcontrol-daemon and ssh from there? ssh in ssh ?
        #subprocess.call(["docker-machine ssh "+args.machine+" \"], shell=True)
        # !! TODO
        r = requests.get(daemon+"/machines/ssh/"+args.machine)
        return r.text
