# Couch Potato GUI

The project is a web based implementation of couch potato.

## Requirements
- Python 3
- Virtualenv
- GCC
- Git
- MongoDB
- SQLite

### Ubuntu 18+
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv python3-dev build-essential git mongodb libmysqlclient-dev -y
```

## Installation

```bash
cd python-cp-gui
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
# Configure config-bos-mint.yaml
cd couchpotato
cp example-config-bos-mint.yaml config-bos-mint.yaml
```

### First Run

```bash
cd python-cp-gui
source env/bin/activate
cd couchpotato/scripts/
./install.sh
```

This operation will clear all the existing users

## Usage

```bash
cd python-cp-gui
source env/bin/activate
cd couchpotato
python3 manage.py runserver 0.0.0.0:9010
```

The instance will now be available at  localhost:9010 if running from the local machine
or at ip_of_the__machine:9010 for any machine.

## Docs
openAPI 2.0 documentation is available at /swagger and /redoc

## Uninsallation
Delete the python-cp-gui folder

## TLS
To run development cerver with TLS
python3 manage.py runsslserver 0.0.0.0:9020

To generate self signed certificates
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt

To run with certificates
python3 manage.py runsslserver 0.0.0.0:9020 --certificate tls.crt --key tls.key 



