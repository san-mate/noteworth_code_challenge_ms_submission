#!/usr/bin/env sh
# Getting static files for Admin panel hosting!
#./manage.py collectstatic --noinput
uwsgi --http "0.0.0.0:8000" --module noteworth_code_challenge.wsgi
