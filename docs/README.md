# Vcontrol API Documentation

## Introduction

vcontrol is the control layer for managing [vent](https://github.com/CyberReboot/vent) instances. It makes programmatically controlling vent possible. vcontrol lets users manage and run multiple instances of vent, accessible through a RESTful Interface and/or a CLI.

The API endpoints allow you to create, start, configure, and run multiple vent instances from one location.

##Accessing the API

After `vcontrol-daemon` is created and running (which is done so by running `make`), use the base URL generated and printed during the `make` process, which looks something like:

`The vcontrol daemon can be accessed here: http://192.168.100.1:29019`

NOTE: This is an example. Your URL may be different from what is printed in this doc.

Copy and paste the URL onto your browser, which in this example is `http://192.168.100.1:29019`.

Documentation
====
- [Docs](https://github.com/CyberReboot/vcontrol/tree/master/docs)
- [Vent Docs](https://github.com/CyberReboot/vent/tree/master/docs)
- [Vent Diagrams](https://github.com/CyberReboot/vent/tree/master/docs/images)

Contributing to Vcontrol
====

Want to contribute?  Awesome!  Issue a pull request or see more details [here](https://github.com/CyberReboot/vcontrol/blob/master/CONTRIBUTING.md).


