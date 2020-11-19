The project is a web based implementation of couch potato.
The project has two parts. An API server and a web interface.

Installation Instructions:

Check out the project

API server:
cd api_server
cd python_cp
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt

cd ../api_server/sports_site
pip3 install -r requirements.txt

Web UI:

cd web_ui
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt

To Run:
API server:
cd api_server
source python_cp/env/bin/activate
cd sports_site
python3 manage.py runserver localhost:8001

Web interface:
cd web_ui
env/bin/gunicorn --bind 0.0.0.0:9010 web_ui.wsgi

The web couch potato is availabe at 
ip_address:9010






