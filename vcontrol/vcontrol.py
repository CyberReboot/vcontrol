#!/usr/bin/env python

import argparse
import ast
import json
import os
import shutil
import subprocess
import sys

# import dependencies
# check for requests module
try:
    import requests
except ImportError:
    print("requests not found, installing...")
    try:
        subprocess.call("pip install requests", shell=True)
        import requests
        print("requests is now installed.")
        print("\n------\n")
    except Exception as e:
        print("requests failed to install", str(e))
        print("Please try installing requests manually.")
        sys.exit(1)

# check for web.py module
try:
    import web
except ImportError:
    print("web.py not found, installing...")
    try:
        subprocess.call("pip install web.py", shell=True)
        import web
        print("web.py is now installed.")
        print("\n------\n")
    except Exception as e:
        print("web.py failed to install", str(e))
        print("Please try installing web.py manually.")
        sys.exit(1)

# cli classes
from cli.version import VersionC

# cli commands classes
from cli.commands.build import BuildCommandC
from cli.commands.clean import CleanCommandC
from cli.commands.deploy import DeployCommandC
from cli.commands.download import DownloadCommandC
from cli.commands.mimetypes import MimetypesCommandC
from cli.commands.generic import GenericCommandC
from cli.commands.info import InfoCommandC
from cli.commands.logs import LogsCommandC
from cli.commands.plugins.add import AddPluginCommandC
from cli.commands.plugins.list_all import ListPluginsCommandC
from cli.commands.plugins.remove import RemovePluginCommandC
from cli.commands.plugins.update import UpdatePluginCommandC
from cli.commands.start import StartCommandC
from cli.commands.stats import StatsCommandC
from cli.commands.status import StatusCommandC
from cli.commands.stop import StopCommandC
from cli.commands.upload import UploadCommandC

# cli machines classes
from cli.machines.boot import BootMachineC
from cli.machines.create import CreateMachineC
from cli.machines.delete import DeleteMachineC
from cli.machines.heartbeat import HeartbeatMachinesC
from cli.machines.list_all import ListMachinesC
from cli.machines.reboot import RebootMachineC
from cli.machines.register import RegisterMachineC
from cli.machines.shutdown import ShutdownMachineC
from cli.machines.ssh import SSHMachineC
from cli.machines.unregister import UnregisterMachineC

# cli providers classes
from cli.providers.add import AddProviderC
from cli.providers.heartbeat import HeartbeatProvidersC
from cli.providers.info import InfoProviderC
from cli.providers.list_all import ListProvidersC
from cli.providers.remove import RemoveProviderC
from cli.providers.stats import StatsProviderC

# rest classes
from rest.index import IndexR
from rest.swagger import SwaggerR
from rest.version import VersionR

# rest commands classes
from rest.commands.build import BuildCommandR
from rest.commands.build import BuildCommandOutputR
from rest.commands.clean import CleanCommandR
from rest.commands.clean import CleanCommandOutputR
from rest.commands.deploy import DeployCommandR
from rest.commands.download import DownloadCommandR
from rest.commands.mimetypes import MimetypesCommandR
from rest.commands.generic import GenericCommandR
from rest.commands.info import InfoCommandR
from rest.commands.logs import LogsCommandR
from rest.commands.plugins.add import AddPluginCommandR
from rest.commands.plugins.list_all import ListPluginsCommandR
from rest.commands.plugins.remove import RemovePluginCommandR
from rest.commands.plugins.update import UpdatePluginCommandR
from rest.commands.start import StartCommandR
from rest.commands.stats import StatsCommandR
from rest.commands.status import StatusCommandR
from rest.commands.stop import StopCommandR
from rest.commands.upload import UploadCommandR

# rest machines classes
from rest.machines.boot import BootMachineR
from rest.machines.create import CreateMachineR
from rest.machines.create import CreateMachineOutputR
from rest.machines.delete import DeleteMachineR
from rest.machines.heartbeat import HeartbeatMachinesR
from rest.machines.list_all import ListMachinesR
from rest.machines.reboot import RebootMachineR
from rest.machines.register import RegisterMachineR
from rest.machines.shutdown import ShutdownMachineR
from rest.machines.ssh import SSHMachineR
from rest.machines.unregister import UnregisterMachineR

# rest providers classes
from rest.providers.add import AddProviderR
from rest.providers.heartbeat import HeartbeatProvidersR
from rest.providers.info import InfoProviderR
from rest.providers.list_all import ListProvidersR
from rest.providers.remove import RemoveProviderR
from rest.providers.stats import StatsProviderR

class VControlServer(object):
    """
    This class is responsible for initializing the urls and web server.
    """
    # need __new__ for tests, but fails to call __init__ when actually running
    def __new__(*args, **kw):
        if hasattr(sys, '_called_from_test'):
            print("don't call __init__")
        else: # pragma: no cover
            return object.__new__(*args, **kw)

    def __init__(self, port=8080, host="0.0.0.0"): # pragma: no cover
        vc_inst = VControl()
        urls = vc_inst.urls()
        # test for dependencies if run locally
        env = None
        try:
            # if set (in Dockerfile) should be VCONTROL_ENV=docker
            env = subprocess.check_output("env | grep VCONTROL_ENV | tee", shell=True).strip('\n')
            if '=' in env:
                env = env.split('=')[1]
        except Exception:
            print("Error loading environment.")
            sys.exit(1)

        # VCONTROL_ENV is only 'docker' if vcontrol-daemon is run in a container
        if env != 'docker':
            # check for docker
            try:
                docker = subprocess.call("which docker", shell=True)
                if docker != 0:
                    print("You must have docker to run vcontrol. Please install docker.")
                    sys.exit(1)
                print("...found docker")
            except Exception:
                print("Error checking for docker. Do you have docker installed?")
                sys.exit(1)

            # check for docker-machine
            try:
                docker_machine = subprocess.call("which docker-machine", shell=True)
                if docker_machine != 0:
                    print("You must have docker-machine to run vcontrol. Please install docker.")
                    sys.exit(1)
                print("...found docker-machine")
            except Exception:
                print("Error checking for docker-machine. Do you have docker-machine installed?")

            # check that docker env is configured
            try:
                is_dockerhost = subprocess.call("env | grep DOCKER_HOST", shell=True)
                # check if call failed
                if is_dockerhost != 0:
                    print("No DOCKER_HOST environment variable set.")
                    print("...assuming localhost.")
                else:
                    docker_host = subprocess.check_output("env | grep DOCKER_HOST", shell=True).strip('\n')
                    docker_urls = subprocess.check_output("docker-machine ls --filter State=Running | grep -v URL | awk \"{print \$5}\"", shell=True).rstrip('\n').split('\n')
                    docker_machine = False
                    for url in docker_urls:
                        if url in docker_host:
                            docker_machine = True
                            print("...found DOCKER_HOST")
                    if not docker_machine:
                        print("A DOCKER_HOST is specified, but no docker-machine was found matching the host.")
                        print("DOCKER_HOST=", docker_host)
                        print("DOCKER-MACHINE URLs=", docker_urls)
                        print("...assuming localhost instead.")
            except Exception:
                print("Error finding DOCKER_HOST. Please set DOCKER_HOST.")
                sys.exit(1)
        # remove test results for runtime
        try:
            os.remove("../.coverage")
        except OSError:
            pass
        app = web.application(urls, globals())
        web.httpserver.runsimple(app.wsgifunc(), (host, port))

class VControl:
    def urls(self):
        # !! TODO rewrite urls to make more logical sense, add missing ones
        urls = (
            '/swagger.yaml', SwaggerR,
            '/v1', IndexR,
            '/v1/', IndexR,
            '/v1/commands/build/(.+)/(.+)', BuildCommandR,
            '/v1/commands/build_output/(.+)/(.+)', BuildCommandOutputR,
            '/v1/commands/clean/(.+)/(.+)/(.+)', CleanCommandR,
            '/v1/commands/clean_output/(.+)/(.+)/(.+)', CleanCommandOutputR,
            '/v1/commands/deploy/(.+)', DeployCommandR,
            '/v1/commands/download', DownloadCommandR,
            '/v1/commands/mimetypes/(.+)/(.+)', MimetypesCommandR,
            '/v1/commands/generic/(.+)', GenericCommandR,
            '/v1/commands/info/(.+)', InfoCommandR,
            '/v1/commands/logs/(.+)', LogsCommandR,
            '/v1/commands/plugins/list/(.+)', ListPluginsCommandR,
            '/v1/commands/plugin/add', AddPluginCommandR,
            '/v1/commands/plugin/remove', RemovePluginCommandR,
            '/v1/commands/plugin/update', UpdatePluginCommandR,
            '/v1/commands/start/(.+)/(.+)', StartCommandR,
            '/v1/commands/stats/(.+)/(.+)/(.+)', StatsCommandR,
            '/v1/commands/status/(.+)/(.+)', StatusCommandR,
            '/v1/commands/stop/(.+)/(.+)', StopCommandR,
            '/v1/commands/upload/(.+)', UploadCommandR,
            '/v1/machines/boot/(.+)', BootMachineR,
            '/v1/machines/create/(.+)', CreateMachineR,
            '/v1/machines/create_output/(.+)', CreateMachineOutputR,
            '/v1/machines/delete/(.+)', DeleteMachineR,
            '/v1/machines/heartbeat', HeartbeatMachinesR,
            '/v1/machines/list', ListMachinesR,
            '/v1/machines/reboot/(.+)', RebootMachineR,
            '/v1/machines/register', RegisterMachineR,
            '/v1/machines/shutdown/(.+)', ShutdownMachineR,
            '/v1/machines/unregister/(.+)', UnregisterMachineR,
            '/v1/providers/add', AddProviderR,
            '/v1/providers/heartbeat', HeartbeatProvidersR,
            '/v1/providers/info/(.+)', InfoProviderR,
            '/v1/providers/list', ListProvidersR,
            '/v1/providers/remove/(.+)', RemoveProviderR,
            '/v1/providers/stats/(.+)', StatsProviderR,
            '/v1/version', VersionR
        )
        return urls

    def main(self, daemon, open_d, api_v):
        privileged = 0
        try:
            r = requests.get('http://localhost:8080'+api_v)
            if r.text == 'vcontrol':
                privileged = 1
        except:
            pass
        if open_d == "true":
            privileged = 1

        try:
            import pkg_resources
            version = pkg_resources.get_distribution('vcontrol').version
        except:
            pass

        # generate cli and parse args
        parser = argparse.ArgumentParser(prog='vcontrol',
                                         description='vcontrol: a command line interface for managing Vent machines')
        subparsers = parser.add_subparsers()
        commands_parser = subparsers.add_parser('commands',
                                                help='Run commands specific to a Vent machine')
        commands_subparsers = commands_parser.add_subparsers()
        daemon_parser = subparsers.add_parser('daemon',
                                              help='Run the vcontrol daemon for making calls over HTTP')
        daemon_parser.set_defaults(which='daemon_parser')
        machines_parser = subparsers.add_parser('machines',
                                                help='Control the creation of management of Vent machines')
        machines_subparsers = machines_parser.add_subparsers()
        providers_parser = subparsers.add_parser('providers',
                                                 help='Control infrastructure for running Vent machines on')
        providers_subparsers = providers_parser.add_subparsers()
        version_parser = subparsers.add_parser('version',
                                               help='Prints out the version of vcontrol')
        version_parser.set_defaults(which='version_parser')

        # commands subparsers
        cmd_build_parser = commands_subparsers.add_parser('build',
                                                          help="Build all containers of a namespace on a Vent machine")
        cmd_build_parser.set_defaults(which='cmd_build_parser')
        cmd_build_parser.add_argument('machine',
                                      help='Machine name to build containers on')
        cmd_build_parser.add_argument('namespace',
                                      choices=['core',
                                               'visualization',
                                               'active',
                                               'passive',
                                               'all'],
                                      help='Category of namespace to build')
        cmd_build_parser.add_argument('--no-cache',
                                      action='store_true',
                                      default=False,
                                      help='Build containers without using cache')
        cmd_clean_parser = commands_subparsers.add_parser('clean',
                                                          help="Clean all containers of a namespace on a Vent machine")
        cmd_clean_parser.set_defaults(which='cmd_clean_parser')
        cmd_clean_parser.add_argument('machine',
                                      help='Machine name to clean containers on')
        cmd_clean_parser.add_argument('namespace',
                                      choices=['core',
                                               'visualization',
                                               'active',
                                               'passive',
                                               'all'],
                                      help='Category of namespace to clean')
        deploy_parser = commands_subparsers.add_parser('deploy',
                                                       help='Deploy a template to a Vent machine')
        deploy_parser.set_defaults(which='deploy_parser')
        deploy_parser.add_argument('machine',
                                   help='Machine name to deploy template to')
        deploy_parser.add_argument('path',
                                   help='File path of template to deploy')
        download_parser = commands_subparsers.add_parser('download',
                                                         help='Download a template from a Vent machine')
        download_parser.set_defaults(which='download_parser')
        download_parser.add_argument('machine',
                                     help='Machine name to download template from')
        download_parser.add_argument('template',
                                     help='Template name to download')
        cmd_generic_parser = commands_subparsers.add_parser('generic',
                                                            help="Generic command to execute on the Vent machine")
        cmd_generic_parser.set_defaults(which='cmd_generic_parser')
        cmd_generic_parser.add_argument('machine',
                                        help='Machine name to execute command on')
        cmd_generic_parser.add_argument('command',
                                        help='Command to execute')
        info_commands_parser = commands_subparsers.add_parser('info',
                                                              help='Get info on a Vent machine')
        info_commands_parser.set_defaults(which='info_commands_parser')
        info_commands_parser.add_argument('machine',
                                          help='Machine name to get info from')
        logs_commands_parser = commands_subparsers.add_parser('logs',
                                                              help='Get logs on a Vent machine')
        logs_commands_parser.add_argument('machine',
                                          help='Machine name to get logs from')
        logs_commands_parser.set_defaults(which='logs_commands_parser')
        # parser for retrieving supported mimetypes or installed namespaces in vent
        mimetypes_parser = commands_subparsers.add_parser('mimetypes', help='Mimetypes a container can process')
        mimetypes_parser.set_defaults(which='mimetypes_parser')
        mimetypes_parser.add_argument('machine', help='Machine name to get mimetypes from')
        mimetypes_parser.add_argument('command',
                                      choices=['mimetypes'],
                                      help='Print from installed namespaces, mimetypes supported, or more...')
        plugin_parser = commands_subparsers.add_parser('plugins',
                                                       help="Perform operations on plugins")
        plugin_subparsers = plugin_parser.add_subparsers()
        add_plugin_parser = plugin_subparsers.add_parser('add',
                                                         help="Add a new plugin")
        add_plugin_parser.add_argument('machine',
                                       help='Machine name to add plugin to')
        add_plugin_parser.add_argument('url',
                                       help='Specify an HTTPS Git URL for the repository that containers plugins')
        add_plugin_parser.add_argument('--username', '-u',
                                          help='Specify your git username for private repos. Without --password arg, you will be prompted for your password')
        add_plugin_parser.add_argument('--password', '-p',
                                          help='Specify your git password for private repos')
        add_plugin_parser.set_defaults(which='add_plugin_parser')
        list_plugin_parser = plugin_subparsers.add_parser('list',
                                                          help="List installed plugins")
        list_plugin_parser.add_argument('machine',
                                       help='Machine name to list plugins installed')
        list_plugin_parser.set_defaults(which='list_plugin_parser')
        remove_plugin_parser = plugin_subparsers.add_parser('remove',
                                                            help="Remove a plugin")
        remove_plugin_parser.add_argument('machine',
                                          help='Machine name to remove plugin from')
        remove_plugin_parser.add_argument('url',
                                          help='Specify an HTTPS Git URL for the repository of plugins to remove')
        remove_plugin_parser.set_defaults(which='remove_plugin_parser')
        update_plugin_parser = plugin_subparsers.add_parser('update',
                                                            help="Update a plugin")
        update_plugin_parser.add_argument('machine',
                                          help='Machine name to update plugin on')
        update_plugin_parser.add_argument('url',
                                          help='Specify an HTTPS Git URL for the repository of plugins to update')
        update_plugin_parser.add_argument('--username', '-u',
                                          help='Specify your git username for private repos. Without --password arg, you will be prompted for your password')
        update_plugin_parser.add_argument('--password', '-p',
                                          help='Specify your git password for private repos')
        update_plugin_parser.set_defaults(which='update_plugin_parser')
        cmd_start_parser = commands_subparsers.add_parser('start',
                                                         help="Start containers in a category on a Vent machine")
        cmd_start_parser.set_defaults(which='cmd_start_parser')
        cmd_start_parser.add_argument('machine',
                                      help='Machine name to start containers on')
        cmd_start_parser.add_argument('containers',
                                      choices=['core',
                                               'visualization',
                                               'active',
                                               'passive',
                                               'all'],
                                      help='Category of containers to start')
        stats_commands_parser = commands_subparsers.add_parser('stats',
                                                               help='Get stats of a Vent machine')
        stats_commands_parser.set_defaults(which='stats_commands_parser')
        stats_commands_parser.add_argument('machine',
                                           help='Machine name to get stats from')
        stats_commands_parser.add_argument('category',
                                           choices=['all', 'running'],
                                           help='Set of containers to get stats of')
        stats_commands_parser.add_argument('format',
                                           choices=['regular', 'json'],
                                           help='Format of output')
        # plugin status parser
        status_parser = commands_subparsers.add_parser('status',
                                                       help="Status of containers and images")
        status_parser.add_argument('machine',
                                    help='Machine name to get status of plugins on')
        status_parser.add_argument('category',
                                    choices=['all',
                                             'containers',
                                             'images',
                                             'disabled',
                                             'errors'],
                                    help='Category of statuses')
        status_parser.set_defaults(which='status_parser')
        cmd_stop_parser = commands_subparsers.add_parser('stop',
                                                         help="Stop containers in a category on a Vent machine")
        cmd_stop_parser.set_defaults(which='cmd_stop_parser')
        cmd_stop_parser.add_argument('machine',
                                     help='Machine name to stop containers on')
        cmd_stop_parser.add_argument('containers',
                                     choices=['core',
                                              'visualization',
                                              'active',
                                              'passive',
                                              'all'],
                                     help='Category of containers to stop')
        upload_parser = commands_subparsers.add_parser('upload',
                                                       help='Upload a file to a Vent machine to be processed')
        upload_parser.set_defaults(which='upload_parser')
        upload_parser.add_argument('machine',
                                   help='Machine name to upload file to')
        upload_parser.add_argument('path',
                                   help='Path to file to upload')
        # machines subparsers
        boot_parser = machines_subparsers.add_parser('boot',
                                                     help='Boot a Vent machine')
        boot_parser.set_defaults(which='boot_parser')
        boot_parser.add_argument('machine',
                                 help='Machine name to boot')
        create_parser = machines_subparsers.add_parser('create',
                                                       help='Create a new Vent machine')
        create_parser.set_defaults(which='create_parser')
        create_parser.add_argument('machine',
                                   help='Machine name to create')
        create_parser.add_argument('provider',
                                   help='Provider to create machine on')
        create_parser.add_argument('--iso', '-i', default="/tmp/vent/vent.iso", type=str,
                                   help='URL to ISO, if left as default, it will pull down the lastest release from GitHub')
        create_parser.add_argument('--group', '-g', default="vent", type=str,
                                   help='Group Vent machine belongs to (default: Vent)')
        create_parser.add_argument('--labels', '-l', default="", type=str,
                                   help='Additional label pairs for the Vent machine (default: "", examples would be "foo=bar,key=val")')
        create_parser.add_argument('--cpus', '-c', default=1, type=int,
                                   help='Number of cpus to create the machine with (default: 1)')
        create_parser.add_argument('--disk-size', '-d', default=20000, type=int,
                                   help='Disk space in MBs to create the machine with (default: 20000)')
        create_parser.add_argument('--memory', '-m', default=1024, type=int,
                                   help='Memory in MBs to create the machine with (default: 1024)')
        delete_parser = machines_subparsers.add_parser('delete',
                                                       help='Delete a Vent machine')
        delete_parser.set_defaults(which='delete_parser')
        delete_parser.add_argument('machine',
                                   help='Machine name to delete')
        delete_parser.add_argument('--force', '-f',
                                   action='store_true',
                                   default=False,
                                   help='Force remove machine of Vent')
        hb_machines_parser = machines_subparsers.add_parser('heartbeat',
                                                            help='Send a heartbeat to all machines')
        hb_machines_parser.set_defaults(which='hb_machines_parser')
        ls_machines_parser = machines_subparsers.add_parser('list',
                                                            help='List all Vent machines')
        ls_machines_parser.set_defaults(which='ls_machines_parser')
        ls_machines_parser.add_argument('--fast', '-f',
                                        action='store_true',
                                        default=False,
                                        help='Get the list fast, without verifying')
        reboot_parser = machines_subparsers.add_parser('reboot',
                                                       help="Reboot a Vent machine")
        reboot_parser.set_defaults(which='reboot_parser')
        reboot_parser.add_argument('machine',
                                   help='Machine name to reboot')
        register_parser = machines_subparsers.add_parser('register',
                                                         help='Register an existing Vent machine')
        register_parser.set_defaults(which='register_parser')
        register_parser.add_argument('machine',
                                     help='Machine name to register')
        register_parser.add_argument('ip',
                                     help='IP address of Vent machine to register')
        register_parser.add_argument('--password', '-p', default='tcuser',
                                     help='Password to log into docker user on Vent with (default: tcuser)')
        shutdown_parser = machines_subparsers.add_parser('shutdown',
                                                         help='Shutdown a Vent machine')
        shutdown_parser.set_defaults(which='shutdown_parser')
        shutdown_parser.add_argument('machine',
                                     help='Machine name to shutdown')
        ssh_parser = machines_subparsers.add_parser('ssh',
                                                    help="SSH to a Vent machine")
        ssh_parser.set_defaults(which='ssh_parser')
        ssh_parser.add_argument('machine',
                                help='Machine name to SSH into')
        unregister_parser = machines_subparsers.add_parser('unregister',
                                                           help='Unregister a Vent machine')
        unregister_parser.set_defaults(which='unregister_parser')
        unregister_parser.add_argument('machine',
                                       help='Machine name to unregister')

        # providers subparsers
        if privileged:
            add_parser = providers_subparsers.add_parser('add',
                                                         help="Add new infrastructure to run Vent machines on")
            add_subparsers = add_parser.add_subparsers()
            # purposefully don't include hyper-v, fusion, etc.
            add_aws_parser = add_subparsers.add_parser('aws',
                                                       help="Public Amazon Web Services")
            add_aws_parser.add_argument('--name', '-n', default='aws',
                                        help='Specify a name for the provider credentials')
            add_aws_parser.add_argument('args',
                                        help='Quoted args needed for docker-machine to deploy on aws')
            add_aws_parser.set_defaults(which='add_aws_parser')
            add_azure_parser = add_subparsers.add_parser('azure',
                                                         help="Public Microsoft cloud")
            add_azure_parser.add_argument('--name', '-n', default='azure',
                                          help='Specify a name for the provider credentials')
            add_azure_parser.add_argument('args',
                                          help='Quoted args needed for docker-machine to deploy on azure')
            add_azure_parser.set_defaults(which='add_azure_parser')
            add_digitalocean_parser = add_subparsers.add_parser('digitalocean',
                                                                help="Public DigitalOcean cloud")
            add_digitalocean_parser.add_argument('--name', '-n', default='digitalocean',
                                                 help='Specify a name for the provider credentials')
            add_digitalocean_parser.add_argument('args',
                                                 help='Quoted args needed for docker-machine to deploy on digitalocean')
            add_digitalocean_parser.set_defaults(which='add_digitalocean_parser')
            add_exoscale_parser = add_subparsers.add_parser('exoscale',
                                                            help="Public Exoscale cloud")
            add_exoscale_parser.add_argument('--name', '-n', default='exoscale',
                                             help='Specify a name for the provider credentials')
            add_exoscale_parser.add_argument('args',
                                             help='Quoted args needed for docker-machine to deploy on exoscale')
            add_exoscale_parser.set_defaults(which='add_exoscale_parser')
            add_google_parser = add_subparsers.add_parser('google',
                                                          help="Public Google cloud")
            add_google_parser.add_argument('--name', '-n', default='google',
                                           help='Specify a name for the provider credentials')
            add_google_parser.add_argument('args',
                                           help='Quoted args needed for docker-machine to deploy on google')
            add_google_parser.set_defaults(which='add_google_parser')
            add_openstack_parser = add_subparsers.add_parser('openstack',
                                                             help="Private OpenStack cloud")
            add_openstack_parser.add_argument('--name', '-n', default='openstack',
                                              help='Specify a name for the provider credentials')
            add_openstack_parser.add_argument('--max-cpu-usage', '-c', default=80, type=int,
                                              help='Max percentage of cpus that can be used and still create machines (default: 80)')
            add_openstack_parser.add_argument('--max-ram-usage', '-r', default=80, type=int,
                                              help='Max percentage of memory that can be used and still create machines (default: 80)')
            add_openstack_parser.add_argument('--max-disk-usage', '-d', default=80, type=int,
                                              help='Max percentage of disk that can be used and still create machines (default: 80)')
            add_openstack_parser.add_argument('args',
                                              help='Quoted args needed for docker-machine to deploy on openstack')
            add_openstack_parser.set_defaults(which='add_openstack_parser')
            add_rackspace_parser = add_subparsers.add_parser('rackspace',
                                                             help="Public Rackspace cloud")
            add_rackspace_parser.add_argument('--name', '-n', default='rackspace',
                                              help='Specify a name for the provider credentials')
            add_rackspace_parser.add_argument('args',
                                              help='Quoted args needed for docker-machine to deploy on rackspace')
            add_rackspace_parser.set_defaults(which='add_rackspace_parser')
            add_softlayer_parser = add_subparsers.add_parser('softlayer',
                                                             help="Public IBM cloud")
            add_softlayer_parser.add_argument('--name', '-n', default='softlayer',
                                              help='Specify a name for the provider credentials')
            add_softlayer_parser.add_argument('args',
                                              help='Quoted args needed for docker-machine to deploy on softlayer')
            add_softlayer_parser.set_defaults(which='add_softlayer_parser')
            add_virtualbox_parser = add_subparsers.add_parser('virtualbox',
                                                              help="Virtualbox for testing, run daemon locally not in a Docker container")
            add_virtualbox_parser.add_argument('--name', '-n', default='virtualbox',
                                               help='Specify a name for the local provider')
            add_virtualbox_parser.set_defaults(which='add_virtualbox_parser')
            add_vmware_parser = add_subparsers.add_parser('vmware',
                                                          help="Private VMWare vSphere cloud")
            add_vmware_parser.add_argument('--name', '-n', default='vmware',
                                           help='Specify a name for the provider credentials')
            add_vmware_parser.add_argument('args',
                                           help='Quoted args needed for docker-machine to deploy on vmware')
            add_vmware_parser.add_argument('--max-cpu-usage', '-c', default=80, type=int,
                                           help='Max percentage of cpus that can be used and still create machines (default: 80)')
            add_vmware_parser.add_argument('--max-ram-usage', '-r', default=80, type=int,
                                           help='Max percentage of memory that can be used and still create machines (default: 80)')
            add_vmware_parser.add_argument('--max-disk-usage', '-d', default=80, type=int,
                                           help='Max percentage of disk that can be used and still create machines (default: 80)')
            add_vmware_parser.set_defaults(which='add_vmware_parser')

        hb_providers_parser = providers_subparsers.add_parser('heartbeat',
                                                              help='Send a heartbeat to all providers')
        hb_providers_parser.set_defaults(which='hb_providers_parser')
        info_providers_parser = providers_subparsers.add_parser('info',
                                                                help='Get info on a provider')
        info_providers_parser.set_defaults(which='info_providers_parser')
        info_providers_parser.add_argument('provider',
                                           help='Provider name to get info from')
        ls_providers_parser = providers_subparsers.add_parser('list',
                                                              help='List all providers')
        ls_providers_parser.set_defaults(which='ls_providers_parser')
        if privileged:
            remove_parser = providers_subparsers.add_parser('remove',
                                                            help='Remove a provider')
            remove_parser.set_defaults(which='remove_parser')
            remove_parser.add_argument('provider',
                                       help='Provider to remove')
        stats_providers_parser = providers_subparsers.add_parser('stats',
                                                                 help='Get stats of a provider')
        stats_providers_parser.set_defaults(which='stats_providers_parser')
        stats_providers_parser.add_argument('provider',
                                            help='Provider name to get stats from')

        args = parser.parse_args()
        if args.which != "daemon_parser":
            if not daemon:
                print("Environment variable VCONTROL_DAEMON not set, defaulting to http://localhost:8080")
                daemon = 'http://localhost:8080'
            try:
                r = requests.get(daemon+api_v)
                if r.text == 'vcontrol':
                    #print "daemon running and reachable!"
                    pass
                else:
                    sys.exit()
            except:
                print("unable to reach the daemon, please start one and set VCONTROL_DAEMON in your environment")
                sys.exit()

        daemon = daemon+api_v

        output = ""
        if privileged:
            if args.which == "remove_parser": output = RemoveProviderC().remove(args, daemon)
            if args.which == "add_aws_parser": output = AddProviderC().add("amazonec2", args, daemon)
            if args.which == "add_azure_parser": output = AddProviderC().add("azure", args, daemon)
            if args.which == "add_digitalocean_parser": output = AddProviderC().add("digitalocean", args, daemon)
            if args.which == "add_exoscale_parser": output = AddProviderC().add("exoscale", args, daemon)
            if args.which == "add_google_parser": output = AddProviderC().add("google", args, daemon)
            if args.which == "add_openstack_parser": output = AddProviderC().add("openstack", args, daemon)
            if args.which == "add_rackspace_parser": output = AddProviderC().add("rackspace", args, daemon)
            if args.which == "add_softlayer_parser": output = AddProviderC().add("softlayer", args, daemon)
            if args.which == "add_virtualbox_parser": output = AddProviderC().add("virtualbox", args, daemon)
            if args.which == "add_vmware_parser": output = AddProviderC().add("vmwarevsphere", args, daemon)

        if args.which == "cmd_build_parser": output = BuildCommandC().build(args, daemon)
        elif args.which == "cmd_generic_parser": output = GenericCommandC().generic(args, daemon)
        elif args.which == "reboot_parser": output = RebootMachineC().reboot(args, daemon)
        elif args.which == "ssh_parser": output = SSHMachineC().ssh(args, daemon)
        elif args.which == "cmd_start_parser": output = StartCommandC().start(args, daemon)
        elif args.which == "cmd_clean_parser": output = CleanCommandC().clean(args, daemon)
        elif args.which == "cmd_stop_parser": output = StopCommandC().stop(args, daemon)
        elif args.which == "create_parser": output = CreateMachineC().create(args, daemon)
        elif args.which == "daemon_parser": output = VControlServer().app.run()
        elif args.which == "delete_parser": output = DeleteMachineC().delete(args, daemon)
        elif args.which == "deploy_parser": output = DeployCommandC().deploy(args, daemon)
        elif args.which == "unregister_parser": output = UnregisterMachineC().unregister(args, daemon)
        elif args.which == "download_parser": output = DownloadCommandC().download(args, daemon)
        elif args.which == "hb_machines_parser": output = HeartbeatMachinesC().heartbeat(args, daemon)
        elif args.which == "hb_providers_parser": output = HeartbeatProvidersC().heartbeat(args, daemon)
        elif args.which == "info_commands_parser": output = InfoCommandC().info(args, daemon)
        elif args.which == "info_providers_parser": output = InfoProviderC().info(args, daemon)
        elif args.which == "ls_machines_parser": output = ListMachinesC().list_all(args, daemon)
        elif args.which == "ls_providers_parser": output = ListProvidersC().list_all(args, daemon)
        elif args.which == "register_parser": output = RegisterMachineC().register(args, daemon)
        elif args.which == "stats_commands_parser": output = StatsCommandC().stats(args, daemon)
        elif args.which == "stats_providers_parser": output = StatsProviderC().stats(args, daemon)
        elif args.which == "version_parser": output = VersionC().version(args, daemon)
        elif args.which == "boot_parser": output = BootMachineC().boot(args, daemon)
        elif args.which == "shutdown_parser": output = ShutdownMachineC().shutdown(args, daemon)
        elif args.which == "add_plugin_parser": output = AddPluginCommandC().add(args, daemon)
        elif args.which == "remove_plugin_parser": output = RemovePluginCommandC().remove(args, daemon)
        elif args.which == "update_plugin_parser": output = UpdatePluginCommandC().update(args, daemon)
        elif args.which == "status_parser": output = StatusCommandC().status(args, daemon)
        elif args.which == "list_plugin_parser": output = ListPluginsCommandC().list_all(args, daemon)
        elif args.which == "logs_commands_parser": output = LogsCommandC().logs(args, daemon)
        elif args.which == "upload_parser": output = UploadCommandC().upload(args, daemon)
        elif args.which == "mimetypes_parser": output = MimetypesCommandC().retrieve(args, daemon)
        else: pass # should never get here

        print(output)

        return

if __name__ == '__main__': # pragma: no cover
    daemon = os.environ.get('VCONTROL_DAEMON')
    if not daemon:
        daemon = "http://localhost:8080"
    open_d = os.environ.get('VCONTROL_OPEN')
    api_v = os.environ.get('VCONTROL_API_VERSION')
    if not api_v:
        api_v = "/v1"
    vc_inst = VControl()
    vc_inst.main(daemon, open_d, api_v)
