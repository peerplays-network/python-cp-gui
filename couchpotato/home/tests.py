from django.test import TestCase

# Create your tests here.
import json
from django.shortcuts import render


def Test(request):
    # events = requests.get('http://s3.jemshid.com:8001/sports/api/game/?filter=events')
    # list_values = dict(enumerate(eval(events.text) , start=1))
    f = open('home/events.json',) 
    data = json.load(f)
    return render(request, 'test.html',{"data": data})