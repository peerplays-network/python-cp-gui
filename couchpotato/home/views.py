 
# Create your views here.
from django.http import Http404 , JsonResponse
from django.shortcuts import render
import json
import requests
import pytz, datetime
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from home.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from game.views import GetEvents , Create , Update

def Test(request):
    # events = requests.get('http://s3.jemshid.com:8001/sports/api/game/?filter=events')
    # list_values = dict(enumerate(eval(events.text) , start=1))
    f = open('home/events.json',) 
    data = json.load(f)
    return render(request, 'test.html',{"data": data})
 
def AuthenticateUser(request):
    if request.method == 'POST': 
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('/')  

def LogoutUser(request):
    logout(request)
    return redirect('/')

def SignUp(request):
    if request.method == 'POST':   
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'register.html',{'form':form})


def Register(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        form = SignUpForm()
        return render(request, 'register.html',{'form':form})

def UpdateList(request):
    if request.user.is_authenticated:
        params = {'filter':'events'}
        events = GetEvents(params)
        list_values = dict(enumerate(events , start=1))
        return render(request, 'update_new.html',{"data": list_values})
    else:
         return render(request, 'login.html')
 

def Home(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')

def CreateList(request,num=1):
    list_values = {}
    start_val = 1
    heading = ''
    is_last = False
    if num == 1:
        games = GetEvents()
        list_values = dict(enumerate(games , start=start_val))
        heading = "Select Games"
    if num  == 2:
        params = {'sport':request.session['sport'].strip()}
        sport = GetEvents(params)
        heading = "Select Event Groups"
        list_values = dict(enumerate(sport , start=start_val))
    if num == 3:
        params = {"sport":request.session['sport'].strip(),"eventGroup":request.session['eventGroup'].strip()}
        teams = GetEvents(params)
        heading = "Home"
        list_values = dict(enumerate(teams , start=start_val))
    if num == 4:
        params ={"sport":request.session['sport'].strip(),"eventGroup":request.session['eventGroup'].strip()}
        teams = GetEvents(params)
        heading = "Away"
        list_values = dict(enumerate(teams , start=start_val))
    if num == 5:
        heading = "Time"
        is_last = True
        
 
    return render(request, 'create.html', {"list" : list_values , 'heading' : heading , "islast":is_last,'question_id':num})


def CreatePost(request):
    question_id = request.POST.get("id")
    option_text = request.POST.get("optiontext")
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
        print("Data " , data)
        result = Create(data)
        if(len(result) > 0 and 'error' not in result):
            return JsonResponse({'success':'Posted'})
        else:
            JsonResponse({'success':'Error','message':result['error']})
    return JsonResponse({'success':True,'message':'success'})



def UpdatePost(request):
    event = request.POST.get("event")
    call = request.POST.get("call")
    home_score = request.POST.get("homeScore")
    away_score = request.POST.get("awayScore")
    data = {'event':eval(event),'call':call,'homeScore':home_score,'awayScore':away_score}
    print(data)
    # JsonResponse({'success':'Error'})
    result = Update(data)
    print(result)
    # result= eval(result.text)
    if(len(result) == 0) :
        return JsonResponse({'success':'Update Done as ' + call})
    else:
        JsonResponse({'success':'Error'})
