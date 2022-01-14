#!/bin/bash

export FLASK_APP=main.py
export FLASK_DEBUG=1
source venv/bin/activate
flask run -h 0.0.0.0 -p 5050