#!/bin/bash

cd ..

#echo 'Activating Virtual Environment'
#source ../_stage_env/bin/activate

echo 'Make Migrations in progress'
python3 manage.py makemigrations

echo 'Migrating'
python3  manage.py migrate

echo 'Pre app settings installing...'
python3 initial_app_settings.py
