#!/usr/bin/env bash
exec gunicorn -w 4 -b ${GUNICORN_DSN} src.wsgi_app:app
