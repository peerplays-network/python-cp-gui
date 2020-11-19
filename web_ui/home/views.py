# Create your views here.
from django.http import Http404 , JsonResponse
from django.shortcuts import render
import json
import requests
import pytz, datetime

urlApi = "http://localhost:8001/" 


def update_new(request):
     
    # f = open('home/events.json',) 
    # data = json.load(f) 
    # events = requests.get('http://s3.jemshid.com:8001/sports/api/game/?filter=events')
    events = requests.get('http://127.0.0.1:8001/sports/api/game/?filter=events')
    # events = requests.get(urlApi + 'sports/api/game/?filter=events')
    list_values = dict(enumerate(eval(events.text) , start=1))
    # print(list_values)
    return render(request, 'update_new.html',{"data": list_values})

def update(request):
      
    events = requests.get('http://s3.jemshid.com:8001/sports/api/game/?filter=events')
    list_values = dict(enumerate(eval(events.text) , start=1))
    print(list_values)
    return render(request, 'update.html',{"data": list_values})

def home(request):
    return render(request, 'index.html')

def create(request,num=1):
    
    # f = open('home/questions.json',) 
    # data = json.load(f) 
    # return render(request, 'create.html',data[num-1])
    list_values = {}
    start_val = 1
    heading = ''
    is_last = False
    if num == 1:
        # games = requests.get('http://s3.jemshid.com:8001/sports/api/game/')
        games = requests.get(urlApi + '/sports/api/game/')
        list_values = dict(enumerate(eval(games.text) , start=start_val))
        heading = "Select Games"
    if num  == 2:
        request_url =  'http://s3.jemshid.com:8001/sports/api/game/?sport=' + request.session['sport'].strip()
        sport = requests.get(request_url)
        heading = "Select Event Groups"
        list_values = dict(enumerate(eval(sport.text) , start=start_val))
    if num == 3:
        request_url =  'http://s3.jemshid.com:8001/sports/api/game/'
        teams = requests.get(request_url,params ={"sport":request.session['sport'].strip(),"eventGroup":request.session['eventGroup'].strip()})
        heading = "Home"
        list_values = dict(enumerate(eval(teams.content) , start=start_val))
    if num == 4:
        request_url =  'http://s3.jemshid.com:8001/sports/api/game/'
        teams = requests.get(request_url,params ={"sport":request.session['sport'].strip(),"eventGroup":request.session['eventGroup'].strip()})
        heading = "Away"
        list_values = dict(enumerate(eval(teams.text) , start=start_val))
    if num == 5:
        heading = "Time"
        is_last = True
        
        # print(request.session['sport'] , request.session['eventGroup'],  request.session['home'] , request.session['away'] , request.session['startTime'])
 
    return render(request, 'create.html', {"list" : list_values , 'heading' : heading , "islast":is_last,'question_id':num})


def post_create(request):
    question_id = request.POST.get("id")
    # option_value = request.POST.get("optionvalue")
    option_text = request.POST.get("optiontext")
    # print("Question Id " , question_id)
    # print("Option Value ",option_value , "   Option Text : ",option_text )
    question_id = int(question_id)
    if question_id == 1:
        request.session['sport'] = option_text
    elif question_id == 2:
        request.session['eventGroup'] = option_text
    elif question_id == 3:
        request.session['home'] = option_text
    elif question_id == 4:
        request.session['away'] = option_text
    elif question_id == 5:
        request.session['startTime'] = option_text
        data = {"sport":request.session['sport'].strip() ,"eventGroup":request.session['eventGroup'].strip(),"home":request.session['home'].strip(),"away":request.session['away'].strip(),"startTime":request.session['startTime'].strip()}
        # print(request.session['sport'] , request.session['eventGroup'],  request.session['home'] , request.session['away'] , request.session['startTime'])
        print("Data " , data)
        result = requests.post('http://s3.jemshid.com:8001/sports/api/game/', data = data)
        if(len(eval(result.text)) > 0):
            return JsonResponse({'success':'Posted','message':result.text})
        else:
            JsonResponse({'success':'Error','message':result.text})
        # print(len(eval(result.text))
    return JsonResponse({'success':True,'message':'success'})



def post_update(request):
    event = request.POST.get("event")
    call = request.POST.get("call")
    home_score = request.POST.get("homeScore")
    away_score = request.POST.get("awayScore")
    print("Event " , eval(event))
    print("\n others " , call , ' home ' , int(home_score) , ' away ', int(away_score))
    data = {'event':eval(event),'call':call,'homeScore':int(home_score),'awayScore':int(away_score)}
    print("Data ",data)
    # result = requests.put('http://s3.jemshid.com:8001/sports/api/game/', data = json.dumps(data),headers = {'Content-Type': 'application/json'})
    result = requests.put(urlApi + 'sports/api/game/', data = json.dumps(data),headers = {'Content-Type': 'application/json'})
    print(result.text)
    result= eval(result.text)
    if(len(result) > 0):
        return JsonResponse({'success':'Update Done as ' + call,'message':result['status']})
    else:
        JsonResponse({'success':'Error','message':result['status']})
