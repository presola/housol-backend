#!/bin/bash

./init.sh

gunicorn housol.wsgi:application --workers 4 --timeout 360 -b 0.0.0.0:8000 --reload
