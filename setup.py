#!/usr/bin/env python2.7
from setuptools import setup

setup(
  name='vcontrol',
  version='0.3.1',
  author='Chiraag Prafullchandra',
  author_email='cprafullchandra@iqt.org',
  maintainer='Charlie Lewis',
  maintainer_email='clewis@iqt.org',
  description='Vent control layer for managing Vent instances',
  long_description=open('README.md').read(),
  url='https://github.com/CyberReboot/vcontrol',
  packages=['vcontrol', 'vcontrol.cli', 'vcontrol.rest', 'vcontrol.cli.commands',
            'vcontrol.cli.commands.plugins', 'vcontrol.cli.machines', 'vcontrol.cli.providers',
            'vcontrol.rest.commands', 'vcontrol.rest.commands.plugins', 'vcontrol.rest.helpers',
            'vcontrol.rest.machines', 'vcontrol.rest.providers'],
  scripts=['bin/vcontrol'],
  include_package_data=True,
  data_files=[('vcontrol/api', ['api/Dockerfile', 'api/index.html', 'api/swagger-ui.js']),
              ('vcontrol/docs', ['docs/README.md']),
              ('vcontrol', ['AUTHORS', 'CHANGELOG.md', 'CONTRIBUTING.md', 'Dockerfile',
               'LICENSE', 'Makefile', 'MAINTAINERS', 'README.md']),
              ('vcontrol/vcontrol', ['vcontrol/requirements.txt', 'vcontrol/swagger.yaml',
               'vcontrol/vmware-stats'])],
  license='LICENSE',
  classifiers=[
    'Programming Language :: Python',
    'Operating System :: POSIX :: Linux',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Environment :: Other Environment'
  ],
  install_requires=[
    'requests',
    'web.py'
  ]
)
