# vcontrol
Control layer for managing vent instances

# getting started

## build and run the vcontrol daemon
```
$ git clone https://github.com/CyberReboot/vcontrol.git
$ cd vcontrol
$ make
```

## using the client
```
# get the daemon URL from the output of make
$ export VENT_CONTROL_DAEMON=http://<dockerhost>:<assignedport>
$ cd vcontrol/bin
$ ./vcontrol -h
```
First you'll want to add a new provider, for example a VMWare vSphere host (note you'll need to make sure you have licensing to be able to make API calls to it).  Since adding and removing providers are a protected command by default, we're going to execute the command from the container rather than the client (it can be done from the client if both the daemon and the client have the environment variable `VENT_CONTROL_OPEN` set to `true`):
```
$ docker exec -it vcontrol-daemon vcontrol providers add -h
```

That will show the options required, where `args` is just taking options from `docker-machine` and inserting them.  For VMWare we're going to want to use at least the following flags:
```
--vmwarevsphere-datacenter ha-datacenter
--vmwarevsphere-datastore datastore1
--vmwarevsphere-network "VM Network"
--vmwarevsphere-vcenter 192.168.100.1
--vmwarevsphere-username domain\\\\username
--vmwarevsphere-password <mypassword>
```

Once we have those, we can simply throw those all into the `args` field at the end as a string, like so:
```
$ docker exec -it vcontrol-daemon vcontrol providers add vmware --name esxihost1 \
 "--vmwarevsphere-datacenter ha-datacenter \
  --vmwarevsphere-datastore datastore1 \
  --vmwarevsphere-network "VM Network" \
  --vmwarevsphere-vcenter 192.168.100.1 \
  --vmwarevsphere-username domain\\\\username \
  --vmwarevsphere-password <mypassword>"
```

Now a listing of providers from the client should show that it has been added successfully:
```
$ ./vcontrol providers list
{'esxihost1':'vmwarevsphere'}
```

Once a provider is added you won't need your credentials again to start making instances of Vent.  To do so, simply execute the following:
```
$ ./vcontrol machines create vent1 esxihost1
```

That will then create a new VM on your VMWare vSphere host that is running the Vent OS.  `commands` can then be run against that host.
