#!/bin/bash
exec gunicorn --config /app/config.py app.wsgi:app