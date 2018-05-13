#export FLASK_APP=app.py 
#export AUTHLIB_INSECURE_TRANSPORT=1
#export FLASK_DEBUG=1
##flask initdb
#flask run --host 192.168.102.184 --port 50000 
uwsgi --ini oauth2-provider.ini
