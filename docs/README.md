# Vcontrol API Documentation

## Introduction

vcontrol is the control layer for managing [vent](https://github.com/CyberReboot/vent) instances. It makes programmatically controlling vent possible. vcontrol lets users manage and run multiple instances of vent, accessible through a RESTful Interface and/or a CLI.

The API endpoints allow you to create, start, configure, and run multiple vent instances from one location.

## Accessing the Swagger UI

After `vcontrol-daemon` is created and running (which is done so by running `make`), use the base URL generated and printed during the `make` process, which looks something like:

`The API can be accessed here: http://192.168.100.1:29019`

NOTE: This is an example. Your URL may be different from what is printed in this doc.

Copy and paste the URL onto your browser, which in this example is `http://192.168.100.1:29019`.

## Accessing the CLI

There is a CLI which, when called, makes the REST calls for the user. Ultimately, both the RESTful interface and the CLI make REST calls, but the CLI is a nice way to make programmatic calls to the REST API.

After running make in the outer-most directory of the repository, execute these commands:

```
# get the daemon URL from the output of make
$ export VCONTROL_DAEMON=http://<dockerhost>:<assignedport>
$ cd vcontrol/bin
$ ./vcontrol -h
```

# API Endpoints

## Commands

### Deploy

*Description*: This endpoint is for uploading a template file to a machine.

Request:
```
URL:          /commands/deploy/{machine}
HTTP Method:  POST
Attributes:   machine - name of machine to deploy template to
```

### Info

*Description*: This endpoint is for getting info about a machine.

Request:
```
URL:          /commands/info/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to get info for
```

### Stats

*Description*: This endpoint is for getting stats about a machine.

Request:
```
URL:          /commands/stats/{machine}/{category}/{format}
HTTP Method:  GET
Attributes:   machine - name of machine to get stats for, category - status of containers to get stats of: [all, running], format - how the output should be formatted: [regular, json]
```

### Logs

*Description*: This endpoint is for retrieving logs from a machine.

Request:
```
URL:          /commands/logs/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to get logs from
```

### Build

*Description*: This endpoint is building Docker images on a machine.

Request:
```
URL:          /commands/build/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to build images on
```

### Generic

*Description*: This endpoint is for running an arbitrary command on a machine and getting the result back.

Request:
```
URL:          /commands/generic/{machine}
HTTP Method:  POST
Attributes:   machine - name of machine to execute the command on
```

### Start Containers

*Description*: This endpoint is for starting a specified category of containers on a specific machine.

Request:
```
URL:          /commands/start/{machine}/{category}
HTTP Method:  GET
Attributes:   machine - name of machine to start containers on
              category - name of category of containers to start
```

### Stop Containers

*Description*: This endpoint is for stopping a specified category of containers on a specific machine.

Request:
```
URL:          /commands/stop/{machine}/{category}
HTTP Method:  GET
Attributes:   machine - name of machine to stop containers on
              category - name of category of containers to stop
```

## Machines

### Create

*Description*: This endpoint is for creating a new machine of vent on a provider.

Request:
```
URL:          /machines/create
HTTP Method:  POST
Attributes:   body
```

Body Schema:

The body should be formatted a specific way. For example:

```
{
  "name": "vent1",
  "provider": "esxi1",
  "group": "vent",
  "labels": "foo=bar,key=val",
  "memory": 4096,
  "cpus": 4,
  "disk_size": 20000
}
```

### Delete

*Description*: This endpoint is for delete an existing machine of vent.

Request:
```
URL:          /machines/delete/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to remove
```

### Register

*Description*: This endpoint is for registering an existing vent machine into vcontrol.

Request:
```
URL:          /machines/register
HTTP Method:  POST
```

### Unregister

*Description*: This endpoint is for unregistering a machine from vcontrol.

Request:
```
URL:          /machines/unregister/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to unregister
```

### Heartbeat

*Description*: This endpoint is just a quick way to ensure that providers are still reachable.

Request:
```
URL:          /machines/heartbeat
HTTP Method:  GET
```

### List

*Description*: This endpoint lists all of the machines that have been created or registered.

Request:
```
URL:          /machines/list
HTTP Method:  GET
```

### Boot

*Description*: This endpoint is for booting a shutdown machine.

Request:
```
URL:          /machines/boot/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to boot
```

### Shutdown

*Description*: This endpoint is for shutting down a running machine.

Request:
```
URL:          /machines/shutdown/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to shutdown
```

### Reboot

*Description*: This endpoint is for rebooting a running machine.

Request:
```
URL:          /machines/reboot/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to reboot
```

### SSH

*Description*: This endpoint is not implemented yet. This endpoint is to SSH into a machine.

Request:
```
URL:          /machines/ssh/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to SSH into
```

## Meta

### /

*Description*: This endpoint is just a quick way to ensure that the vcontrol API is up and running properly.

Request:
```
URL:          /
HTTP Method:  GET
```

### /version

*Description*: This endpoint return the version of vcontrol that is currently running this API.

Request:
```
URL:          /version
HTTP Method:  GET
```

## Providers

### Add

*Description*: This endpoint allows for a new provider such as openstack or vmware to be added. A vent machine runs on a provider. Note that a provider can only be added from localhost of the machine running vcontrol unless the environment variable VCONTROL_OPEN=true is set on the server.

Request:
```
URL:          /providers/add
HTTP Method:  POST
Attributes:   body
```
Body Schema:

The body should be formatted a specific way. For example:

```
{
  "name": "esxi1",
  "provider": "openstack",
  "args": "",
  "ram": 80,
  "cpu": 80,
  "disk": 80
}
```

### Heartbeat

*Description*: This endpoint is just a quick way to ensure that providers are still reachable.

Request:
```
URL:          /providers/heartbeat
HTTP Method:  GET
```

### List

*Description*: This endpoint lists all of the providers that have been added.

Request:
```
URL:          /providers/list
HTTP Method:  GET
```

### Remove

*Description*: This endpoint allows for removing a provider such as openstack or vmware. A vent machine runs on a provider, this will not remove existing vent machines on the specified provider. Note that a provider can only be removed from localhost of the machine running vcontrol unless the environment variable VCONTROL_OPEN=true is set on the server.

Request:
```
URL:          /providers/remove/{provider}
HTTP Method:  GET
Attributes:   provider - Name of provider to remove
```
