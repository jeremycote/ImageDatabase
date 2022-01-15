#!/bin/bash

source venv/bin/activate
gunicorn --bind :5050 --workers 1 --threads 2 --timeout 0 src.main:app