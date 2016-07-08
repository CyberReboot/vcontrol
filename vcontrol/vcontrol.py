#!/usr/bin/env python

import argparse
import ast
import json
import os
import requests
import shutil
import subprocess
import sys
import web

# cli classes
from cli.version import VersionC

# rest classes
from rest.index import IndexR
from rest.swagger import SwaggerR
from rest.version import VersionR

# rest commands classes
from rest.commands.build import BuildCommandR
from rest.commands.clean import CleanCommandR
from rest.commands.deploy import DeployCommandR
from rest.commands.download import DownloadCommandR
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
from rest.machines.delete import DeleteMachineR
from rest.machines.deregister import DeregisterMachineR
from rest.machines.heartbeat import HeartbeatMachinesR
from rest.machines.list_all import ListMachinesR
from rest.machines.reboot import RebootMachineR
from rest.machines.register import RegisterMachineR
from rest.machines.shutdown import ShutdownMachineR
from rest.machines.ssh import SSHMachineR

# rest providers classes
from rest.providers.add import AddProviderR
from rest.providers.heartbeat import HeartbeatProvidersR
from rest.providers.info import InfoProviderR
from rest.providers.list_all import ListProvidersR
from rest.providers.remove import RemoveProviderR
from rest.providers.stats import StatsProviderR

def get_urls():
    # !! TODO rewrite urls to make more logical sense, add missing ones
    urls = (
        '/swagger.yaml', SwaggerR,
        '/v1', IndexR,
        '/v1/', IndexR,
        '/v1/add_provider', AddProviderR,
        '/v1/remove_provider/(.+)', RemoveProviderR,
        '/v1/create_machine', CreateMachineR,
        '/v1/delete_machine/(.+)', DeleteMachineR,
        '/v1/boot_machine/(.+)', BootMachineR,
        '/v1/shutdown_machine/(.+)', ShutdownMachineR,
        '/v1/command_build/(.+)', BuildCommandR,
        '/v1/command_generic/(.+)', GenericCommandR,
        '/v1/command_reboot/(.+)', RebootMachineR,
        '/v1/command_start/(.+)/(.+)', StartCommandR,
        '/v1/command_stop/(.+)/(.+)', StopCommandR,
        '/v1/heartbeat_machines', HeartbeatMachinesR,
        '/v1/heartbeat_providers', HeartbeatProvidersR,
        '/v1/list_machines', ListMachinesR,
        '/v1/list_providers', ListProvidersR,
        '/v1/get_stats_commands/(.+)', StatCommandR,
        '/v1/get_stats_providers/(.+)', StatsProviderR,
        '/v1/get_info_commands/(.+)', InfoCommandR,
        '/v1/get_info_providers/(.+)', InfoProviderR,
        '/v1/get_logs/(.+)', LogsCommandR,
        '/v1/deploy_template/(.+)', DeployCommandR,
        '/v1/get_template', DownloadCommandR,
        '/v1/register_machine', RegisterMachineR,
        '/v1/deregister_machine/(.+)', DeregisterMachineR,
        '/v1/version', VersionR
    )
    return urls

def daemon_mode(args):
    sys.argv[1:] = ['0.0.0.0','8080']
    urls = get_urls()
    app = web.application(urls, globals())
    app.run()
    return True

def add_provider(provider, args, daemon):
    # only privileged can add providers, which currently is only
    # accessible from the server running the vcontrol daemon
    open_d = os.environ.get('VENT_CONTROL_OPEN')
    if open_d != "true":
        # daemon as passed in is: 'http:..../'+api_v
        # split and get the end and append
        api_v = daemon.split('/')[-1]
        daemon = 'http://localhost:8080/'+api_v
    if provider == "virtualbox":
        payload = {'name': args.name, 'provider': provider}
    else:
        payload = {'name': args.name, 'provider': provider, 'args': args.args}
    if provider == "openstack" or provider == "vmwarevsphere":
        payload['cpu'] = str(args.max_cpu_usage)
        payload['ram'] = str(args.max_ram_usage)
        payload['disk'] = str(args.max_disk_usage)
    r = requests.post(daemon+"/add_provider", data=json.dumps(payload))
    return r.text

def remove_provider(args, daemon):
    # only privileged can remove providers, which currently is only
    # accessible from the server running the vcontrol daemon
    open_d = os.environ.get('VENT_CONTROL_OPEN')
    if open_d != "true":
        # daemon as passed in is: 'http:..../'+api_v
        # split and get the end and append
        api_v = daemon.split('/')[-1]
        daemon = 'http://localhost:8080/'+api_v
    r = requests.get(daemon+"/remove_provider/"+args.provider)
    return r.text

def create_machine(args, daemon):
    # first ssh into the machine running vcontrol daemon
    # from there use docker-machine to provision
    payload = {}
    payload['machine'] = args.machine
    payload['provider'] = args.provider
    payload['cpus'] = args.cpus
    payload['disk_size'] = args.disk_size
    payload['iso'] = args.iso
    payload['memory'] = args.memory
    payload['group'] = args.group
    payload['labels'] = args.labels

    r = requests.post(daemon+"/create_machine", data=json.dumps(payload))
    return r.text

def delete_machine(args, daemon):
    # check if controlled by docker-machine, if not fail
    # first ssh into the machine running vcontrol daemon
    # from there use docker-machine to delete
    payload = {'force':args.force}
    r = requests.get(daemon+"/delete_machine/"+args.machine, params=payload)
    return r.text

def start_machine(args, daemon):
    # check if controlled by docker-machine, if not fail
    # first ssh into the machine running vcontrol daemon
    # from there use docker-machine to start
    r = requests.get(daemon+"/start_machine/"+args.machine)
    return r.text

def stop_machine(args, daemon):
    # check if controlled by docker-machine, if not fail
    # first ssh into the machine running vcontrol daemon
    # from there use docker-machine to stop
    r = requests.get(daemon+"/stop_machine/"+args.machine)
    return r.text

def boot_machine(args, daemon):
    r = requests.get(daemon+"/boot_machine/"+args.machine)
    return r.text

def shutdown_machine(args, daemon):
    r = requests.get(daemon+"/shutdown_machine/"+args.machine)
    return r.text

def command_build(args, daemon):
    payload = {'no_cache':args.no_cache}
    r = requests.get(daemon+"/command_build/"+args.machine, params=payload)
    return r.text

def command_generic(args, daemon):
    payload = {'command':args.command}
    r = requests.post(daemon+"/command_generic/"+args.machine, data=json.dumps(payload))
    return r.text

def command_reboot(args, daemon):
    r = requests.get(daemon+"/command_reboot/"+args.machine)
    return r.text

def command_ssh(args, daemon):
    # get the certs from the machine running vcontrol daemon
    # from there ssh to the machine, whether with docker-machine or ssh

    # !! TODO check if controlled by docker-machine, if not fail (all machines should be controlled by docker-machine)
    #subprocess.call(["docker-machine ssh "+args.machine], shell=True)
    # !! TODO
    return True

def command_start(args, daemon):
    r = requests.get(daemon+"/command_start/"+args.machine+"/"+args.containers)
    return r.text

def command_stop(args, daemon):
    r = requests.get(daemon+"/command_stop/"+args.machine+"/"+args.containers)
    return r.text

def command_messages(args, daemon):
    r = requests.get(daemon+"/command_messages/"+args.machine)
    return r.text

def command_services(args, daemon):
    r = requests.get(daemon+"/command_services/"+args.machine)
    return r.text

def command_tasks(args, daemon):
    r = requests.get(daemon+"/command_tasks/"+args.machine)
    return r.text

def command_tools(args, daemon):
    r = requests.get(daemon+"/command_tools/"+args.machine)
    return r.text

def command_types(args, daemon):
    r = requests.get(daemon+"/command_types/"+args.machine)
    return r.text

def heartbeat_machines(args, daemon):
    r = requests.get(daemon+"/heartbeat_machines")
    return r.text

def heartbeat_providers(args, daemon):
    r = requests.get(daemon+"/heartbeat_providers")
    return r.text

def list_machines(args, daemon):
    payload = {'fast':args.fast}
    r = requests.get(daemon+"/list_machines", params=payload)
    return r.text

def list_providers(args, daemon):
    r = requests.get(daemon+"/list_providers")
    return r.text

def get_stats_commands(args, daemon):
    r = requests.get(daemon+"/get_stats/"+args.machine)
    return r.text

def get_stats_providers(args, daemon):
    r = requests.get(daemon+"/get_stats/"+args.provider)
    return r.text

def get_info_providers(args, daemon):
    r = requests.get(daemon+"/get_info_providers/"+args.provider)
    return r.text

def get_info_commands(args, daemon):
    r = requests.get(daemon+"/get_info_commands/"+args.machine)
    return r.text

def get_logs(args, daemon):
    r = requests.get(daemon + "/get_logs/"+args.machine)
    return r.text

def get_template(args, daemon):
    payload = {}
    payload['machine'] = args.machine
    payload['filename'] = args.filename
    r = requests.get(daemon+"/get_template", data=payload)
    return r.text

def deploy_template(args, daemon):
    files = {'myfile': open(args.path, 'rb')}
    # !! TODO how does files work with swagger?
    r = requests.post(daemon+"/deploy_template/"+args.machine, files=files)
    return True

def register_machine(args, daemon):
    # use default or supply credentials
    # use generic driver from docker-machine
    # note that they will be sent to the vcontrol daemon
    payload = {}
    payload['machine'] = args.machine
    payload['ip'] = args.ip
    payload['password'] = args.password
    r = requests.post(daemon+"/register_machine", data=json.dumps(payload))
    return r.text

def deregister_machine(args, daemon):
    r = requests.get(daemon+"/deregister_machine/"+args.machine)
    return r.text

def main(daemon, open_d, api_v):
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
        with open('VERSION', 'r') as f: version = f.read().strip()
    except:
        with open('../VERSION', 'r') as f: version = f.read().strip()

    # generate cli and parse args
    parser = argparse.ArgumentParser(description='vcontrol: a command line interface for managing Vent machines')
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
    logs_commands_parser.set_defaults(which='logs_commands_parser')
    plugin_parser = commands_subparsers.add_parser('plugins',
                                                     help="Perform operations on plugins")
    plugin_subparsers = plugin_parser.add_subparsers()
    add_plugin_parser = plugin_subparsers.add_parser('add',
                                                     help="Add a new plugin")
    add_plugin_parser.add_argument('url',
                                   help='Specify an HTTPS Git URL for the repository that containers plugins')
    add_plugin_parser.set_defaults(which='add_plugin_parser')
    list_plugin_parser = plugin_subparsers.add_parser('list',
                                                     help="List installed plugins")
    list_plugin_parser.set_defaults(which='list_plugin_parser')
    remove_plugin_parser = plugin_subparsers.add_parser('remove',
                                                     help="Remove a plugin")
    remove_plugin_parser.add_argument('url',
                                   help='Specify an HTTPS Git URL for the repository of plugins to remove')
    remove_plugin_parser.set_defaults(which='remove_plugin_parser')
    update_plugin_parser = plugin_subparsers.add_parser('update',
                                                     help="Update a plugin")
    update_plugin_parser.add_argument('url',
                                   help='Specify an HTTPS Git URL for the repository of plugins to update')
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
    status_parser = commands_subparsers.add_parser('status',
                                                     help="Status of containers and images")
    status_subparsers = status_parser.add_subparsers()
    containers_status_parser = status_subparsers.add_parser('containers',
                                                     help="Status of containers")
    containers_status_parser.set_defaults(which='containers_status_parser')
    images_status_parser = status_subparsers.add_parser('images',
                                                     help="Status of images")
    images_status_parser.set_defaults(which='images_status_parser')
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
    create_parser.add_argument('--iso', '-i', default="/tmp/Vent/Vent.iso", type=str,
                               help='URL to ISO, if left as default, it will build the ISO from source')
    create_parser.add_argument('--group', '-g', default="Vent", type=str,
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
    deregister_parser = machines_subparsers.add_parser('deregister',
                                              help='Deregister a Vent machine')
    deregister_parser.set_defaults(which='deregister_parser')
    deregister_parser.add_argument('machine',
                                   help='Machine name to deregister')
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
                                         help='Get stats of a Vent machine')
    stats_providers_parser.set_defaults(which='stats_providers_parser')
    stats_providers_parser.add_argument('provider',
                              help='Provider name to get stats from')

    args = parser.parse_args()
    if args.which != "daemon_parser":
        if not daemon:
            print "Environment variable VENT_CONTROL_DAEMON not set, defaulting to http://localhost:8080"
            daemon = 'http://localhost:8080'
        try:
            r = requests.get(daemon+api_v)
            if r.text == 'vcontrol':
                #print "daemon running and reachable!"
                pass
            else:
                sys.exit()
        except:
            print "unable to reach the daemon, please start one and set VENT_CONTROL_DAEMON in your environment"
            sys.exit()

    daemon = daemon+api_v

    output = ""
    if privileged:
        if args.which == "remove_parser": output = remove_provider(args, daemon)
        if args.which == "add_aws_parser": output = add_provider("amazonec2", args, daemon)
        if args.which == "add_azure_parser": output = add_provider("azure", args, daemon)
        if args.which == "add_digitalocean_parser": output = add_provider("digitalocean", args, daemon)
        if args.which == "add_exoscale_parser": output = add_provider("exoscale", args, daemon)
        if args.which == "add_google_parser": output = add_provider("google", args, daemon)
        if args.which == "add_openstack_parser": output = add_provider("openstack", args, daemon)
        if args.which == "add_rackspace_parser": output = add_provider("rackspace", args, daemon)
        if args.which == "add_softlayer_parser": output = add_provider("softlayer", args, daemon)
        if args.which == "add_virtualbox_parser": output = add_provider("virtualbox", args, daemon)
        if args.which == "add_vmware_parser": output = add_provider("vmwarevsphere", args, daemon)

    if args.which == "cmd_build_parser": output = command_build(args, daemon)
    elif args.which == "cmd_generic_parser": output = command_generic(args, daemon)
    elif args.which == "reboot_parser": output = command_reboot(args, daemon)
    elif args.which == "ssh_parser": output = command_ssh(args, daemon)
    elif args.which == "cmd_start_parser": output = command_start(args, daemon)
    elif args.which == "cmd_stop_parser": output = command_stop(args, daemon)
    elif args.which == "create_parser": output = create_machine(args, daemon)
    elif args.which == "daemon_parser": output = daemon_mode(args)
    elif args.which == "delete_parser": output = delete_machine(args, daemon)
    elif args.which == "deploy_parser": output = deploy_template(args, daemon)
    elif args.which == "deregister_parser": output = deregister_machine(args, daemon)
    elif args.which == "get_template_parser": output = get_template(args, daemon)
    elif args.which == "hb_machines_parser": output = heartbeat_machines(args, daemon)
    elif args.which == "hb_providers_parser": output = heartbeat_providers(args, daemon)
    elif args.which == "info_commands_parser": output = get_info_commands(args, daemon)
    elif args.which == "info_providers_parser": output = get_info_providers(args, daemon)
    elif args.which == "ls_machines_parser": output = list_machines(args, daemon)
    elif args.which == "ls_providers_parser": output = list_providers(args, daemon)
    elif args.which == "register_parser": output = register_machine(args, daemon)
    elif args.which == "start_parser": output = start_machine(args, daemon)
    elif args.which == "stats_commands_parser": output = get_stats_commands(args, daemon)
    elif args.which == "stats_providers_parser": output = get_stats_providers(args, daemon)
    elif args.which == "stop_parser": output = stop_machine(args, daemon)
    elif args.which == "version_parser": output = VersionC().version(args, daemon)
    elif args.which == "boot_parser": output = boot_machine(args, daemon)
    elif args.which == "shutdown_parser": output = shutdown_machine(args, daemon)
    else: pass # should never get here

    print output

    return

if __name__ == '__main__':
    daemon = os.environ.get('VENT_CONTROL_DAEMON')
    if not daemon:
        daemon = "http://localhost:8080"
    open_d = os.environ.get('VENT_CONTROL_OPEN')
    api_v = os.environ.get('VENT_CONTROL_API_VERSION')
    if not api_v:
        api_v = "/v1"
    main(daemon, open_d, api_v)
