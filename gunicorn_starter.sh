#!/bin/sh

gunicorn --bind 0.0.0.0:5000 -w 3 --log-level=debug --timeout 0 --preload  wsgi:app
