 
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
from home.models import ApplicationFeatures 
from django.contrib.auth import logout
from game.views import GetEvents  , CreatePotato , UpdatePotato
from django.contrib.auth.decorators import login_required
from django.core import serializers
from home.utilities import index_page_permitted , register_login_page_permitted , allow_login , allow_register
from django.contrib import messages


def AuthenticateUser(request):
    '''
    param: request
    description: Loads the login page and does the authentication.
    '''

    try:
        if request.method == 'POST': 
            username = request.POST.get('username')
            raw_password = request.POST.get('password')
            user = authenticate(username=username, password=raw_password)
            
            if user is not None:
                if allow_login(request , user):
                    login(request, user)
                    return redirect('/')
                else:
                    return render(request, '403.html')    
            else:
                messages.error(request, 'User name Password Invalid')
        
        return render(request, 'login.html')
    except:
        return render(request, '404.html')

def LogoutUser(request):
    '''
    param: request
    description: Log outs the logged in user
    '''

    logout(request)
    return redirect('/')

def SignUp(request):
    '''
    param: request
    description :  Loads the registration page and does the sign up and authentication.
    '''
    try:
        if allow_register():
            if request.method == 'POST':   
                form = SignUpForm(request.POST)
                if form.is_valid():
                    form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    if user is not None:
                        login(request, user)
                        return redirect('/')
            else:
                form = SignUpForm()
            return render(request, 'register.html',{'form':form})
        else:
            return render(request, '403.html') 

    except:
        return render(request, '404.html')

 
def UpdateList(request):
    '''
    param : request
    description : To load update page
    '''
    try:
        if index_page_permitted(request):
            params = {'filter':'events'}
            events = GetEvents(params)
            list_values = dict(enumerate(events , start=1))
            return render(request, 'update.html',{"data": list_values})
        else:
            return render(request, 'login.html')
    except:
        return render(request, '404.html')

 

def Home(request):
    '''
    param : request
    description : To load home page
    '''

    try:
        if index_page_permitted(request):
            return render(request, 'index.html')
        elif register_login_page_permitted():
            return render(request, 'login.html')
    except:
        return render(request, '404.html')

def CreateList(request,num=1):
    '''
    param-1 : request
    param-2 : num , represents which question to load.
    description : To load list of options during create of a page
    '''
    
    if index_page_permitted(request):
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

    elif register_login_page_permitted():
            return render(request, 'login.html')


def CreatePost(request):
    '''
    param : request
    description : To save Create set options
    '''

    question_id = request.POST.get("id")
    option_text = request.POST.get("optiontext")
    username = request.user.username

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
        data = {"sport":request.session['sport'].strip() ,"eventGroup":request.session['eventGroup'].strip(),"home":request.session['home'].strip(),"away":request.session['away'].strip(),"startTime":request.session['startTime'].strip(),\
                "username":username}
        print("Data " , data)
        result = CreatePotato(data) 

        if(len(result) > 0 and 'error' not in result):
            return JsonResponse({'success':'Posted'})
        else:
            JsonResponse({'success':'Error','message':result['error']})
    return JsonResponse({'success':True,'message':'success'})



def UpdatePost(request):
    '''
    param : request
    description : To update Events
    '''

    event = request.POST.get("event")
    call = request.POST.get("call")
    home_score = request.POST.get("homeScore")
    away_score = request.POST.get("awayScore")
    username = request.user.username
    data = {'event':eval(event),'call':call,'homeScore':home_score,'awayScore':away_score,'username':username}
    result = UpdatePotato(data)
    if(len(result) == 0) :
        return JsonResponse({'success':'Update Done as ' + call})
    else:
        return JsonResponse({'success':'Error'})


def admin(request):
    '''
    param : request
    description : Load admin page
    '''

    if request.user.is_authenticated:
        app_feature = ApplicationFeatures.objects.filter(id=1).first()
        sign_up = None
        limit_user_signup = None
        users = User.objects.filter(is_superuser=False)
        if app_feature is not None:
            sign_up = app_feature.signup
            limit_user_signup = app_feature.limit_user_signup
        return render(request, 'admin.html',{'signup':sign_up,'users':users,'limit_users':limit_user_signup})
    else:
        return render(request, 'login.html')


def SaveApplicationFeatures(request):
    '''
    param : request
    description : Save admin feature signup
    '''

    req_signup = request.POST.get("signup")
    req_limit_users = request.POST.get("limit_users")

    try:
        value_sign = None
        value_user_limit = None
        if req_signup is not '':
            if(req_signup == 'true'):value_sign = True
            else:value_sign = False
            signup, created = ApplicationFeatures.objects.update_or_create(id=1, defaults={'signup':value_sign})
        
        if req_limit_users is not '':
            if(req_limit_users == 'true'):value_user_limit = True
            else:value_user_limit = False
            limit_users, created = ApplicationFeatures.objects.update_or_create(id=1, defaults={'limit_user_signup':value_user_limit})

        return JsonResponse({'success':'Success'})
    except:
        return JsonResponse({'success':'Error'})
    

def SaveUserStatus(request):
    '''
    param : request
    description : Save user login 
    '''

    req_id = request.POST.get("id")
    req_active = request.POST.get("active")
    value = None
    if(req_active == 'true'):value = True
    else:value = False
    try:
        user = User.objects.get(id=req_id)
        user.is_active = value
        user.save()
        return JsonResponse({'success':'Success'})
    except:
        return JsonResponse({'success':'Error'})



