export FLASK_APP=app.py 
export AUTHLIB_INSECURE_TRANSPORT=1
export FLASK_DEBUG=1
flask initdb
flask run --host zteeed.fr --port 50000 
