$env:FLASK_APP = "src/main.py"
$env:FLASK_DEBUG = 1
venv/Scripts/activate
flask run -h 0.0.0.0 -p 5050