# vcontrol
Control layer for managing [vent](https://github.com/CyberReboot/vent) instances

vcontrol makes programmatically controlling vent possible. vcontrol lets users manage and run multiple instances of vent, accessible through a RESTful Interface and/or a CLI.

## Getting Started

### Dependencies
* Docker
* Make
* Additionally if running vcontrol locally:
 * Docker-Machine
 * pip
 * Python

### Build and run the vcontrol daemon
```
$ git clone https://github.com/CyberReboot/vcontrol.git
$ cd vcontrol
$ make
```

From here, it is possible to use the RESTful interface in a browser. To access it, follow the URL listed in the output when running `make`:

e.g.: `The API can be accessed here: https://192.168.100.1:27209`

Copy and paste the link into a browser, and a Swagger UI will pop up with a menu of all vcontrol commands.

## Using the client

An alternative to using the RESTful interface is the CLI, found in the `bin` directory of the repo.

```
# get the daemon URL from the output of make
$ export VCONTROL_DAEMON=http://<dockerhost>:<assignedport>
$ cd vcontrol/bin
$ ./vcontrol -h
```
### Add a provider

First you'll want to add a new provider, for example a VMWare vSphere host (note you'll need to make sure you have licensing to be able to make API calls to it).  Since adding and removing providers are a protected command by default, we're going to execute the command from the container rather than the client (it can be done from the client if both the daemon and the client have the environment variable `VCONTROL_OPEN` set to `true`):
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

**A note on passwords**

The optional argument `--vmwarevsphere-password` is optional, and if it is omitted, the cli will prompt for a password. Whether or not the optional argument is present, passwords must:
* escape any special characters (e.g. pass?word -> pass\?word) with the exception of single quotes('), which are treated as literal without escaping
* contain no spaces

### List all providers

Now a listing of providers from the client should show that it has been added successfully:
```
$ ./vcontrol providers list
{'esxihost1':'vmwarevsphere'}
```
### Create a machine

Once a provider is added you won't need your credentials again to start making instances of Vent.  To do so, simply execute the following:
```
$ ./vcontrol machines create vent1 esxihost1
```

That will then create a new VM on your VMWare vSphere host that is running the Vent OS.  `commands` can then be run against that host.

### Register a machine

Vent instances may already exist on a host machine. To register an existing vent instance to vcontrol, execute the following:
```
$ ./vcontrol machines register vent2 192.168.100.1
```

`192.168.100.1` is the host machine ip where `vent2` is stored. `vent2` is then registered with vcontrol, and commands executed on vcontrol can affect that instance.
