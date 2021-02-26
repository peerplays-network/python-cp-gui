# Couch Potato GUI

The project is a web based implementation of couch potato.

## Installation

```bash 
cd python-cp-gui
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```



### First Run

Modify config-bos-mint.yaml

```bash
source env/bin/activate
cd couchpotato/scripts/
./install.sh
```

This operation will clear all the existing users

## Usage
```bash
source env/bin/activate
cd couchpotato
python3 manage.py runserver localhost:9010
```

The instance will now be available at  localhost:9010 if running from the local machine
or at ip_of_the__machine:9010 for any machine.

## Docs
openAPI 2.0 documentation is available at /swagger and /redoc

## Uninsallation
Delete the python-cp-gui folder


