#!/bin/sh
set -e

cd /opt/project/app
alembic upgrade head
