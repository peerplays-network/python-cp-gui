The project is a web based implementation of couch potato.

Installation Instructions:

Check out the project

cd couchpotato
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt

cd python_cp
pip3 install -r requirements.txt
python3 setup.py install
cd ..


First Run:
cd couchpotato
source python_cp/env/bin/activate
cd scripts/
./install.sh

This operation will clear all the existing users



To Run:
cd couchpotato
source python_cp/env/bin/activate
python3 manage.py runserver localhost:9010

The web couch potato is availabe at 
ip_address:9010
