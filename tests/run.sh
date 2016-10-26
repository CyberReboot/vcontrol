#!/bin/bash
py.test /vcontrol -v --cov=/vcontrol/vcontrol --cov-report term-missing && cp .coverage /local-vent/ chmod 777 /local-vent/.coverage
