#!/bin/bash
py.test /vcontrol -v --cov=/vcontrol/vcontrol --cov-report term-missing && bash <(curl -s https://codecov.io/bash)
