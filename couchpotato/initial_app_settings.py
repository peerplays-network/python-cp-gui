import os,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'couchpotato.settings')
django.setup()
from django.contrib.auth.models import User

try:
    u = User(username='admin')
    u.set_password('admin@1234')
    u.is_superuser = True
    u.is_staff = True
    u.save()

except:
    print("Admin User already Exists")
