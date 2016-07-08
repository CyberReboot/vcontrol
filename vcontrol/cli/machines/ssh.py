class SSHMachineC:
    def ssh(self, args, daemon):
        """
        get the certs from the machine running vcontrol daemon
        from there ssh to the machine, whether with docker-machine or ssh
        """

        # !! TODO check if controlled by docker-machine, if not fail (all machines should be controlled by docker-machine)
        #subprocess.call(["docker-machine ssh "+args.machine], shell=True)
        # !! TODO
        return True
