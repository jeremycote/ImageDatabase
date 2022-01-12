#!/bin/bash

export FLASK_APP=/home/jeremy/Projects/ImageDatabase/main.py
export FLASK_DEBUG=1
source venv/bin/activate
flask run -h http://172.28.13.62/ -p 5000