The project is a web based implementation of couch potato.

Installation Instructions:

Check out the project

cd python-cp-gui
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt

python3 couchpotato/python_cp/setup.py install


First Run:
source env/bin/activate
cd couchpotato/scripts/
./install.sh

This operation will clear all the existing users

To Run:
source env/bin/activate
cd couchpotato
python3 manage.py runserver localhost:9010

The web couch potato is availabe at 
ip_address:9010

openAPI 2.0 documentation is available at /swagger and /redoc

