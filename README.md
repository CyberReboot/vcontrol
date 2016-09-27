# vcontrol
[![PyPI](https://img.shields.io/pypi/v/vcontrol.svg?maxAge=2592000)](https://github.com/CyberReboot/vcontrol)
[![PyPI](https://img.shields.io/pypi/dm/vcontrol.svg?maxAge=2592000)](https://github.com/CyberReboot/vcontrol)

Control layer for managing [vent](https://github.com/CyberReboot/vent) instances

vcontrol makes programmatically controlling vent possible. vcontrol lets users manage and run multiple instances of vent, accessible through a RESTful Interface and/or a CLI.

## Getting Started

### Dependencies

If you are using `vcontrol` as a client:
  * pip

If you are using `vcontrol` as a daemon:
  - If `vcontrol` is running locally:
    * docker-machine
    * pip
  - If `vcontrol` is running in a container:
    * docker
    * docker-machine
    * make
    * pip

### Build and run the vcontrol daemon

1. To install `vcontrol` as a client:

   ```
   $ pip install vcontrol
   $ export VCONTROL_DAEMON=<ip of vcontrol daemon>
   ```

2. To install `vcontrol` as a daemon in a container:

   ```
   $ git clone https://github.com/CyberReboot/vcontrol.git
   $ cd vcontrol
   $ make install # to install vcontrol to your python path
   $ make api
   # the daemon should be reachable at the URL given by make api
   ```

3. To install `vcontrol` as a daemon locally:

  ```
  $ git clone https://github.com/CyberReboot/vcontrol.git
  $ make install
  $ vcontrol daemon # b/c of make install, vcontrol commands can be issued from anywhere
  # the daemon should be running on http://localhost:8080/
  ```

4. To install `vcontrol` client and daemon together:

  Simply install it as a daemon (2 or 3), and perform step 1.

If `vcontrol` was installed via option `2`: it is possible to use the RESTful interface in a browser. To access it, follow the URL listed in the output when running `make api`:

e.g.: `The API can be accessed here: https://192.168.100.1:27209`

Copy and paste the link into a browser, and a Swagger UI will pop up with a menu of all vcontrol commands.

## Using the client

An alternative to using the RESTful interface is the CLI, found in the `bin` directory of the repo.

To connect as the client:
```
$ export VCONTROL_DAEMON=http://<url>:<port> # URL/PORT given from make commands if make was used
$ vcontrol -h # from anywhere
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

The optional argument `--vmwarevsphere-password` is optional (`--openstack-password` if using Openstack), and if it is omitted, the cli will prompt for a password. Whether or not the optional argument is present, passwords must:
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


## Documentation
- [Docs](https://github.com/CyberReboot/vcontrol/tree/master/docs)
- [Vent Docs](https://github.com/CyberReboot/vent/tree/master/docs)
- [Vent Diagrams](https://github.com/CyberReboot/vent/tree/master/docs/images)

## Contributing to Vcontrol

Want to contribute?  Awesome!  Issue a pull request or see more details [here](https://github.com/CyberReboot/vcontrol/blob/master/CONTRIBUTING.md).
