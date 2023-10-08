#!/bin/sh
set -e

cd /opt/project/app
uvicorn app_main:app --host 0.0.0.0 --port 8000
