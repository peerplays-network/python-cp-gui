#!/bin/bash

cd ..

#echo 'Activating Virtual Environment'
#source ../_stage_env/bin/activate


echo 'Make Migrations in progress'
python manage.py makemigrations

echo 'Migrating'
python manage.py migrate

echo 'Pre app settings installing...'
python initial_app_settings.py
