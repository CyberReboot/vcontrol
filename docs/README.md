# Vcontrol API Documentation

## Introduction

vcontrol is the control layer for managing [vent](https://github.com/CyberReboot/vent) instances. It makes programmatically controlling vent possible. vcontrol lets users manage and run multiple instances of vent, accessible through a RESTful Interface and/or a CLI.

The API endpoints allow you to create, start, configure, and run multiple vent instances from one location.

## Installing vcontrol

First of all, there are several ways to install vcontrol. For basic usage as a `user`, we recommend `1` For more advanced usage, i.e - as a `developer`, we recommend `2`.

1. To install vcontrol simply run:
```
$ pip install vcontrol
```

After, you should be able to run `vcontrol -h` and verify vcontrol has installed correctly.

2. Alternatively, you can:
```
$ git clone
$ cd vcontrol
$ make api
# optionally - "make install" to add vcontrol to your python path
```

## Accessing the CLI

There is a CLI which, when called, makes the REST calls for the user. Ultimately, both the RESTful interface and the CLI make REST calls, but the CLI is a nice way to make programmatic calls to the REST API.

After install vcontrol either through `pip install vcontrol` or `make api` in the outer-most directory of the repository, execute these commands:

```
# get the daemon URL from the output of make
$ export VCONTROL_DAEMON=http://<dockerhost>:<assignedport>
# if you installed via pip then run vcontrol -h from anywhere
# if you have not installed or run make install to add vcontrol to your python path do:
$ cd vcontrol/bin
$ ./vcontrol -h
```

## Accessing the Swagger UI

*Note* - the `vcontrol-daemon` is only available inside a running container, which can be generated via `make api`. The UI is unsupported for pip installations.

After `vcontrol-daemon` is created and running (via `make api`), use the base URL generated and printed during the `make api` process, which looks something like:

`The API can be accessed here: http://192.168.100.1:29019`

NOTE: This is an example. Your URL may be different from what is printed in this doc.

Copy and paste the URL onto your browser, which in this example is `http://192.168.100.1:29019`.

# API Endpoints - CLI & rAPI

## Commands

### Build

*Description*: This endpoint is for building the core and plugins on a machine.

Request:
```
URL:          /commands/build/{machine}/{output_type}
HTTP Method:  GET
Attributes:   machine - name of machine to build core + plugins on
              output_type - a for html-friendly output feed, b for plain-text output feed
              body =
              {
                no_cache - option to build with cache or without cache
              }
```

### Clean

*Description*: This endpoint is for cleaning the core + plugin services on a machine.

Request:
```
URL:          /commands/clean/{machine}/{namespace}/{output_type}
HTTP Method:  GET
Attributes:   machine - name of machine to clean services on
              namespace - type of services to clean: [core, passive, active, visualization, all]
              output_type - a for html-friendly output feed, b for plain-text output feed
```

### Deploy

*Description*: This endpoint is for uploading a template file to a machine.

Request:
```
URL:          /commands/deploy/{machine}
HTTP Method:  POST
Attributes:   machine - name of machine to deploy template to
              body =
              {
                path - path to the file to upload
              }
```

### Download

*Description*: This endpoint is for retrieving the template file of a machine.

Request:
```
URL:          /commands/download
HTTP Method:  POST
Attributes:   body =
              {
                machine - name of the machine to download template from,
                template - name of the template to download
              }
```

### Generic

*Description*: This endpoint is for running an arbitrary command on an machine and getting the result back.

Request:
```
URL:          /commands/generic/machine
HTTP Method:  POST
Attributes:   machine - name of the machine to run the generic command on
              body =
              {
                command - the command to run on the machine
              }
```

### Info

*Description*: This endpoint is for getting info about a machine.

Request:
```
URL:          /commands/info/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to get info for
```

### Logs

*Description*: This endpoint is for retrieving machine logs.

Request:
```
URL:          /commands/logs/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to get logs from
```

### Mimetypes

*Description*: This endpoint is for getting the mimetypes and installed namespaces on a Vent machine.

Request:
```
URL:          /commands/mimetypes/{machine}/{command}
HTTP Method:  GET
Attributes:   machine - name of the machine to get the mimetypes from
              command - the command to run: [mimetypes, namespaces] (currently only mimetypes supported)
```

### Start (Containers)

*Description*: This endpoint is for starting a specified category of containers on a specific machine.

Request:
```
URL:          /commands/start/{machine}/{category}
HTTP Method:  GET
Attributes:   machine - name of machine to start containers on
              category - name of category of containers to start
```

### Stats

*Description*: This endpoint is for getting stats about a machine.

Request:
```
URL:          /commands/stats/{machine}/{category}/{format}
HTTP Method:  GET
Attributes:   machine - name of machine to get stats for
              category - status of containers to get stats of: [all, running]
              format - how the output should be formatted: [regular, json]
```

### Stop (Containers)

*Description*: This endpoint is for stopping a specified category of containers on a specific machine.

Request:
```
URL:          /commands/stop/{machine}/{category}
HTTP Method:  GET
Attributes:   machine - name of machine to stop containers on
              category - name of category of containers to stop
```

### Upload

*Description*: This endpoint is for getting uploading a file to a Vent machine to be processed.

Request:
```
URL:          /commands/upload/{machine}
HTTP Method:  POST
Attributes:   machine - name of the machine to upload the file to
              body =
              {
                path - path to the file to upload
              }
```

### Plugins APIs

#### Add

*Description*: This endpoint is for adding a new plugin repository on a Vent machine.

Request:
```
URL:          /commands/plugin/add
HTTP Method:  POST
Attributes:   body =
              {
                machine - machine to add plugin repository to,
                url - url to the repository the plugin is stored at
              }
```

#### List

*Description*: This endpoint is for listing plugins installed on a Vent machine.

Request:
```
URL:          /commands/plugin/list/{machine}
HTTP Method:  GET
Attributes:   machine - the name of the machine to list the installed plugins on
```

#### Remove

*Description*:  This endpoint is for removing a new plugin repository on a Vent machine.

Request:
```
URL:          /commands/plugin/remove
HTTP Method:  POST
Attributes:   body =
              {
                machine - the name of the machine to remove the plugin repository from,
                url - the url of the plugin repository to be removed
              }
```

#### Update

*Description*: This endpoint is for updating an existing plugin repository on a Vent machine.

Request:
```
URL:          /commands/plugin/update
HTTP Method:  POST
Attributes:   body =
              {
                machine - name of the machine to update the plugin on,
                url - the url of the plugin repository to be updated
              }
```

## Machines

### Boot

*Description*: This endpoint is for booting a shutdown machine.

Request:
```
URL:          /machines/boot/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to boot
```

### Create

*Description*: This endpoint is for creating a new machine of vent on a provider.

Request:
```
URL:          /machines/create/{output_type}
HTTP Method:  POST
Attributes:   output_type - a for html-friendly display of the output feed, b for a plain-text display of the output feed
              body =
              {
                machine - name of machine to create,
                provider - name of provider to host machine on,
                cpus,
                disk_size,
                iso,
                memory,
                group,
                labels
              }
Example:
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

*Description*: This endpoint is for deleting an existing machine of vent.

Request:
```
URL:          /machines/delete/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to remove
              body =
              {
                force - force delete the machine or not
              }
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
Attributes:   body =
              {
                fast - whether to get the faster list or a list with more details
              }
```

### Reboot

*Description*: This endpoint is for rebooting a running machine.

Request:
```
URL:          /machines/reboot/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to reboot
```

### Register

*Description*: This endpoint is for registering an existing vent machine into vcontrol.

Request:
```
URL:          /machines/register
HTTP Method:  POST
Attributes:   body =
              {
                machine - name of the machine to register
                ip - the ip of the machine to register
                password - credentials for the operation
              }
```

### Shutdown

*Description*: This endpoint is for shutting down a running machine.

Request:
```
URL:          /machines/shutdown/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to shutdown
```

### SSH

*Description*: This endpoint is not implemented yet. This endpoint is to SSH into a machine.

Request:
```
URL:          /machines/ssh/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to SSH into
```

### Unregister

*Description*: This endpoint is for unregistering a machine from vcontrol.

Request:
```
URL:          /machines/unregister/{machine}
HTTP Method:  GET
Attributes:   machine - name of machine to unregister
```

## Providers

### Add

*Description*: This endpoint allows for a new provider such as openstack or vmware to be added. A vent machine runs on a provider. Note that a provider can only be added from the localhost of the machine running vcontrol unless the environment variable VCONTROL_OPEN=true is set on the server.

Request:
```
URL:          /providers/add
HTTP Method:  POST
Attributes:   body =
              {
                name - name of the provider machine,
                provider - name of the provider (vmware, openstack...),
                args - associated arguments for the provider,
                ram,
                cpu,
                disk
              }
Example:
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

### Info

*Description*: This endpoint is not implemented yet. This endpoint is for getting info about a provider.

Request:
```
URL:          /providers/info/{provider}
HTTP Method:  GET
Attributes:   provider - provider to get info of
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
Attributes:   provider - name of provider to remove
```

### Stats

*Description*: This endpoint is not implemented yet. This endpoint is for getting stats about a provider.

Request:
```
URL:          /providers/stats/{provider}
HTTP Method:  GET
Attributes:   provider - name of provider to get stats of
```

# API Endpoints - rAPI Only

## Meta

### Index

*Description*: This endpoint is just a quick way to ensure that the vcontrol API is up and running properly.

Request:
```
URL:          /
HTTP Method:  GET
```

### Version

*Description*: This endpoint return the version of vcontrol that is currently running this API.

Request:
```
URL:          /version
HTTP Method:  GET
```
