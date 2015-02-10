#!/bin/sh
virtualenv -p python3 .
bin/pip install -r requirements.txt --upgrade
bin/python setup.py develop
