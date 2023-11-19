#!/bin/sh
set -e

pip3 install --upgrade pip
pip3 install -U --force-reinstall --no-cache-dir -r /opt/project/requirements.txt
