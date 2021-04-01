 
# Create your views here.
from django.http import Http404 , JsonResponse , HttpResponseRedirect
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
from game.views import GetEvents  , CreatePotato , UpdatePotato , GetMatchingEvents
from django.contrib.auth.decorators import login_required
from django.core import serializers
from home.utilities import index_page_permitted , register_login_page_permitted , allow_login , allow_register
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm



def AuthenticateUser(request):
    '''
    param: request
    description: Loads the login page and does the authentication.
    '''
    
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').strip()
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                if username is None or username is '':
                    messages.error(request, 'Username cannot be blank')
                else:
                    messages.error(request, "Invalid username or password.")
        else:
            username = request.POST.get('username').strip()
            if username is None or username is '':
                messages.error(request, 'Username cannot be blank')
            else:
                messages.error(request, "Invalid username or password.")
 
    return HttpResponseRedirect('/')


def LogoutUser(request):
    '''
    param: request
    description: Log outs the logged in user
    '''

    logout(request)
    return redirect('/')

def LogoutSwagger(request):
    '''
    param: request
    description: Log outs the logged in user
    '''

    logout(request)
    return redirect('/swagger')


def SignUp(request):
    '''
    param: request
    description :  Loads the registration page and does the sign up and authentication.
    '''
    # print("In sign up ")
    # try:
    if allow_register():
        # print("in allow register " , request.method )
        if request.method == 'POST':   
            form = SignUpForm(request.POST)
            # print(form)
            if form.is_valid():
                # print("Form is valid")
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

    # except:
    #     return render(request, '404.html')

 
def UpdateList(request):
    '''
    param : request
    description : To load update page
    '''
    try:
        if index_page_permitted(request):
            params = {'filter':'events'}
            events = GetEvents(params)
            list_values = {}
            if events is not None:
                list_values = dict(enumerate(events , start=1))
            return render(request, 'update_cp.html',{"data": list_values})
        else:
            return render(request, 'login.html')
    except:
        return render(request, '404.html')

 
def getstaticEvents():
    newDict = [{'eventFromChain': {'id': '1.22.602', 'name': [['en', 'Lazio v Crotone']], 'season': [['en', '']], 'start_time': '2021-03-12T14:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.534', 'name': [['en', 'Augsburg v Mönchengladbach']], 'season': [['en', '']], 'start_time': '2021-03-12T19:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.533', 'name': [['en', 'Augsburg v Mönchengladbach']], 'season': [['en', '']], 'start_time': '2021-03-12T19:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'finished', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.604', 'name': [['en', 'Atalanta v Spezia']], 'season': [['en', '']], 'start_time': '2021-03-12T19:45:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'upcoming', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.603', 'name': [['en', 'Atalanta v Spezia']], 'season': [['en', '']], 'start_time': '2021-03-12T19:45:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'finished', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.490', 'name': [['en', 'Levante v Valencia']], 'season': [['en', '']], 'start_time': '2021-03-12T20:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.766', 'name': [['en', 'Vegas Golden Knights @ St. Louis Blues']], 'season': [['en', '']], 'start_time': '2021-03-13T01:00:00', 'event_group_id': '1.21.0', 'scores': [], 'status': 'finished', 'event_group_name': 'NHL Regular Season', 'sport': 'Ice Hockey'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.645', 'name': [['en', 'Denver Nuggets @ Memphis Grizzlies']], 'season': [['en', '']], 'start_time': '2021-03-13T01:00:00', 'event_group_id': '1.21.5', 'scores': [], 'status': 'finished', 'event_group_name': 'NBA Regular Season', 'sport': 'Basketball'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.646', 'name': [['en', 'Cleveland Cavaliers @ New Orleans Pelicans']], 'season': [['en', '']], 'start_time': '2021-03-13T01:00:00', 'event_group_id': '1.21.5', 'scores': [], 'status': 'finished', 'event_group_name': 'NBA Regular Season', 'sport': 'Basketball'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.763', 'name': [['en', 'Philadelphia 76ers @ Washington Wizards']], 'season': [['en', '']], 'start_time': '2021-03-13T01:00:00', 'event_group_id': '1.21.5', 'scores': [], 'status': 'finished', 'event_group_name': 'NBA Regular Season', 'sport': 'Basketball'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.767', 'name': [['en', 'Los Angeles Kings @ Colorado Avalanche']], 'season': [['en', '']], 'start_time': '2021-03-13T02:00:00', 'event_group_id': '1.21.0', 'scores': [], 'status': 'finished', 'event_group_name': 'NHL Regular Season', 'sport': 'Ice Hockey'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.764', 'name': [['en', 'Miami Heat @ Chicago Bulls']], 'season': [['en', '']], 'start_time': '2021-03-13T02:00:00', 'event_group_id': '1.21.5', 'scores': [], 'status': 'finished', 'event_group_name': 'NBA Regular Season', 'sport': 'Basketball'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.768', 'name': [['en', 'Ottawa Senators @ Edmonton Oilers']], 'season': [['en', '']], 'start_time': '2021-03-13T02:00:00', 'event_group_id': '1.21.0', 'scores': [], 'status': 'finished', 'event_group_name': 'NHL Regular Season', 'sport': 'Ice Hockey'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.769', 'name': [['en', 'San Jose Sharks @ Anaheim Ducks']], 'season': [['en', '']], 'start_time': '2021-03-13T03:00:00', 'event_group_id': '1.21.0', 'scores': [], 'status': 'finished', 'event_group_name': 'NHL Regular Season', 'sport': 'Ice Hockey'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.491', 'name': [['en', 'Alaves v Cadiz']], 'season': [['en', '']], 'start_time': '2021-03-13T13:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.634', 'name': [['en', 'Sassuolo v Verona']], 'season': [['en', '']], 'start_time': '2021-03-13T14:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.653', 'name': [['en', 'Werder Bremen v Bayern Munich']], 'season': [['en', '']], 'start_time': '2021-03-13T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'finished', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-13T14:30:00Z', 'home': 'Werder Bremen', 'away': 'Bayern Munich'}, 'arguments': {'home_score': '1', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:55.104013Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.540', 'name': [['en', 'Union Berlin v FC Koln']], 'season': [['en', '']], 'start_time': '2021-03-13T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-13T14:30:00Z', 'home': 'Union Berlin', 'away': 'FC Koln'}, 'arguments': {'home_score': '2', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:55.188676Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.539', 'name': [['en', 'Union Berlin v FC Koln']], 'season': [['en', '']], 'start_time': '2021-03-13T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'finished', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-13T14:30:00Z', 'home': 'Union Berlin', 'away': 'FC Koln'}, 'arguments': {'home_score': '2', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:55.270535Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.537', 'name': [['en', 'Wolfsburg v Schalke 04']], 'season': [['en', '']], 'start_time': '2021-03-13T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'finished', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.538', 'name': [['en', 'Wolfsburg v Schalke 04']], 'season': [['en', '']], 'start_time': '2021-03-13T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.541', 'name': [['en', 'Mainz v Freiburg']], 'season': [['en', '']], 'start_time': '2021-03-13T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-13T14:30:00Z', 'home': 'Mainz', 'away': 'Freiburg'}, 'arguments': {'home_score': '1', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:55.493435Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.542', 'name': [['en', 'Mainz v Freiburg']], 'season': [['en', '']], 'start_time': '2021-03-13T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-13T14:30:00Z', 'home': 'Mainz', 'away': 'Freiburg'}, 'arguments': {'home_score': '1', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:55.575429Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.652', 'name': [['en', 'Real Madrid v Elche']], 'season': [['en', '']], 'start_time': '2021-03-13T15:15:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.606', 'name': [['en', 'Benevento v Fiorentina']], 'season': [['en', '']], 'start_time': '2021-03-13T17:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'upcoming', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.605', 'name': [['en', 'Benevento v Fiorentina']], 'season': [['en', '']], 'start_time': '2021-03-13T17:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.535', 'name': [['en', 'Dortmund v Hertha']], 'season': [['en', '']], 'start_time': '2021-03-13T17:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'finished', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.536', 'name': [['en', 'Dortmund v Hertha']], 'season': [['en', '']], 'start_time': '2021-03-13T17:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.494', 'name': [['en', 'Osasuna v Valladolid']], 'season': [['en', '']], 'start_time': '2021-03-13T17:30:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.607', 'name': [['en', 'Genoa v Udinese']], 'season': [['en', '']], 'start_time': '2021-03-13T19:45:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'finished', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.608', 'name': [['en', 'Genoa v Udinese']], 'season': [['en', '']], 'start_time': '2021-03-13T19:45:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'upcoming', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.493', 'name': [['en', 'Getafe v Ath Madrid']], 'season': [['en', '']], 'start_time': '2021-03-13T20:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'upcoming', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.492', 'name': [['en', 'Getafe v Ath Madrid']], 'season': [['en', '']], 'start_time': '2021-03-13T20:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'finished', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.727', 'name': [['en', 'Bologna v Sampdoria']], 'season': [['en', '']], 'start_time': '2021-03-14T11:30:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'upcoming', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-14T11:30:00Z', 'home': 'Bologna', 'away': 'Sampdoria'}, 'arguments': {'home_score': '3', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:56.397061Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.726', 'name': [['en', 'Bologna v Sampdoria']], 'season': [['en', '']], 'start_time': '2021-03-14T11:30:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-14T11:30:00Z', 'home': 'Bologna', 'away': 'Sampdoria'}, 'arguments': {'home_score': '3', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:56.460689Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.687', 'name': [['en', 'Southampton v Brighton']], 'season': [['en', '']], 'start_time': '2021-03-14T12:00:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'finished', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-14T12:00:00Z', 'home': 'Southampton', 'away': 'Brighton'}, 'arguments': {'home_score': '1', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:56.464189Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.688', 'name': [['en', 'Southampton v Brighton']], 'season': [['en', '']], 'start_time': '2021-03-14T12:00:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'upcoming', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-14T12:00:00Z', 'home': 'Southampton', 'away': 'Brighton'}, 'arguments': {'home_score': '1', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:56.467013Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.673', 'name': [['en', 'Leverkusen v Bielefeld']], 'season': [['en', '']], 'start_time': '2021-03-14T12:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-14T12:30:00Z', 'home': 'Leverkusen', 'away': 'Bielefeld'}, 'arguments': {'home_score': '1', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:56.540579Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.672', 'name': [['en', 'Leverkusen v Bielefeld']], 'season': [['en', '']], 'start_time': '2021-03-14T12:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-14T12:30:00Z', 'home': 'Leverkusen', 'away': 'Bielefeld'}, 'arguments': {'home_score': '1', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:56.61041Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.660', 'name': [['en', 'Celta Vigo v Ath Bilbao']], 'season': [['en', '']], 'start_time': '2021-03-14T13:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.684', 'name': [['en', 'Leicester v Sheffield United']], 'season': [['en', '']], 'start_time': '2021-03-14T14:00:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'in_progress', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-14T14:00:00Z', 'home': 'Leicester', 'away': 'Sheffield United'}, 'arguments': {'home_score': '5', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:56.692313Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.725', 'name': [['en', 'Parma Calcio 1913 v Roma']], 'season': [['en', '']], 'start_time': '2021-03-14T14:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-14T14:00:00Z', 'home': 'Parma Calcio 1913', 'away': 'Roma'}, 'arguments': {'home_score': '2', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:56.757793Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.724', 'name': [['en', 'Torino v Inter']], 'season': [['en', '']], 'start_time': '2021-03-14T14:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'upcoming', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.723', 'name': [['en', 'Torino v Inter']], 'season': [['en', '']], 'start_time': '2021-03-14T14:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.671', 'name': [['en', 'RasenBallsport Leipzig v Ein Frankfurt']], 'season': [['en', '']], 'start_time': '2021-03-14T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-14T14:30:00Z', 'home': 'RasenBallsport Leipzig', 'away': 'Ein Frankfurt'}, 'arguments': {'home_score': '1', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:56.97345Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.670', 'name': [['en', 'RasenBallsport Leipzig v Ein Frankfurt']], 'season': [['en', '']], 'start_time': '2021-03-14T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-14T14:30:00Z', 'home': 'RasenBallsport Leipzig', 'away': 'Ein Frankfurt'}, 'arguments': {'home_score': '1', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:57.060972Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.664', 'name': [['en', 'Granada v Sociedad']], 'season': [['en', '']], 'start_time': '2021-03-14T15:15:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'upcoming', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-14T15:15:00Z', 'home': 'Granada', 'away': 'Sociedad'}, 'arguments': {'home_score': '1', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:57.114467Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.663', 'name': [['en', 'Granada v Sociedad']], 'season': [['en', '']], 'start_time': '2021-03-14T15:15:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-14T15:15:00Z', 'home': 'Granada', 'away': 'Sociedad'}, 'arguments': {'home_score': '1', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:57.164568Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.681', 'name': [['en', 'Arsenal v Tottenham']], 'season': [['en', '']], 'start_time': '2021-03-14T16:30:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'in_progress', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-14T16:30:00Z', 'home': 'Arsenal', 'away': 'Tottenham'}, 'arguments': {'home_score': '2', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:57.169648Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.682', 'name': [['en', 'Arsenal v Tottenham']], 'season': [['en', '']], 'start_time': '2021-03-14T16:30:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'upcoming', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-14T16:30:00Z', 'home': 'Arsenal', 'away': 'Tottenham'}, 'arguments': {'home_score': '2', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:57.17497Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.667', 'name': [['en', 'Cagliari v Juventus']], 'season': [['en', '']], 'start_time': '2021-03-14T17:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-14T17:00:00Z', 'home': 'Cagliari', 'away': 'Juventus'}, 'arguments': {'home_score': '1', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:57.251487Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.668', 'name': [['en', 'Cagliari v Juventus']], 'season': [['en', '']], 'start_time': '2021-03-14T17:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'upcoming', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-14T17:00:00Z', 'home': 'Cagliari', 'away': 'Juventus'}, 'arguments': {'home_score': '1', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:57.32255Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.734', 'name': [['en', 'Stuttgart v Hoffenheim']], 'season': [['en', '']], 'start_time': '2021-03-14T17:00:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-14T17:00:00Z', 'home': 'Stuttgart', 'away': 'Hoffenheim'}, 'arguments': {'home_score': '2', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:57.401101Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.735', 'name': [['en', 'Stuttgart v Hoffenheim']], 'season': [['en', '']], 'start_time': '2021-03-14T17:00:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-14T17:00:00Z', 'home': 'Stuttgart', 'away': 'Hoffenheim'}, 'arguments': {'home_score': '2', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:57.474476Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.661', 'name': [['en', 'Eibar v Villarreal']], 'season': [['en', '']], 'start_time': '2021-03-14T17:30:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-14T17:30:00Z', 'home': 'Eibar', 'away': 'Villarreal'}, 'arguments': {'home_score': '1', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:57.523987Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.662', 'name': [['en', 'Eibar v Villarreal']], 'season': [['en', '']], 'start_time': '2021-03-14T17:30:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'upcoming', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-14T17:30:00Z', 'home': 'Eibar', 'away': 'Villarreal'}, 'arguments': {'home_score': '1', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:57.583102Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.669', 'name': [['en', 'Milan v Napoli']], 'season': [['en', '']], 'start_time': '2021-03-14T19:45:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-14T19:45:00Z', 'home': 'Milan', 'away': 'Napoli'}, 'arguments': {'home_score': '0', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:57.653676Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.666', 'name': [['en', 'Sevilla v Betis']], 'season': [['en', '']], 'start_time': '2021-03-14T20:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'upcoming', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-14T20:00:00Z', 'home': 'Sevilla', 'away': 'Betis'}, 'arguments': {'home_score': '1', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:57.702612Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.665', 'name': [['en', 'Sevilla v Betis']], 'season': [['en', '']], 'start_time': '2021-03-14T20:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-14T20:00:00Z', 'home': 'Sevilla', 'away': 'Betis'}, 'arguments': {'home_score': '1', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:57.750823Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.715', 'name': [['en', 'Barcelona v Huesca']], 'season': [['en', '']], 'start_time': '2021-03-15T20:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-15T20:00:00Z', 'home': 'Barcelona', 'away': 'Huesca'}, 'arguments': {'home_score': '4', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:57.796495Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.728', 'name': [['en', 'Torino v Sassuolo']], 'season': [['en', '']], 'start_time': '2021-03-17T14:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-17T14:00:00Z', 'home': 'Torino', 'away': 'Sassuolo'}, 'arguments': {'home_score': '3', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:57.860354Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.729', 'name': [['en', 'Torino v Sassuolo']], 'season': [['en', '']], 'start_time': '2021-03-17T14:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'upcoming', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-17T14:00:00Z', 'home': 'Torino', 'away': 'Sassuolo'}, 'arguments': {'home_score': '3', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:57.925802Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.716', 'name': [['en', 'Sevilla v Elche']], 'season': [['en', '']], 'start_time': '2021-03-17T18:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-17T18:00:00Z', 'home': 'Sevilla', 'away': 'Elche'}, 'arguments': {'home_score': '2', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:57.970711Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.717', 'name': [['en', 'Sevilla v Elche']], 'season': [['en', '']], 'start_time': '2021-03-17T18:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'upcoming', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-17T18:00:00Z', 'home': 'Sevilla', 'away': 'Elche'}, 'arguments': {'home_score': '2', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:58.027846Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.674', 'name': [['en', 'Bielefeld v RasenBallsport Leipzig']], 'season': [['en', '']], 'start_time': '2021-03-19T19:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-19T19:30:00Z', 'home': 'Bielefeld', 'away': 'RasenBallsport Leipzig'}, 'arguments': {'home_score': '0', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:58.149687Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.675', 'name': [['en', 'Bielefeld v RasenBallsport Leipzig']], 'season': [['en', '']], 'start_time': '2021-03-19T19:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-19T19:30:00Z', 'home': 'Bielefeld', 'away': 'RasenBallsport Leipzig'}, 'arguments': {'home_score': '0', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:58.235135Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.730', 'name': [['en', 'Parma Calcio 1913 v Genoa']], 'season': [['en', '']], 'start_time': '2021-03-19T19:45:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-19T19:45:00Z', 'home': 'Parma Calcio 1913', 'away': 'Genoa'}, 'arguments': {'home_score': '1', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:58.298623Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.718', 'name': [['en', 'Betis v Levante']], 'season': [['en', '']], 'start_time': '2021-03-19T20:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-19T20:00:00Z', 'home': 'Betis', 'away': 'Levante'}, 'arguments': {'home_score': '2', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:58.344717Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.719', 'name': [['en', 'Betis v Levante']], 'season': [['en', '']], 'start_time': '2021-03-19T20:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'upcoming', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-19T20:00:00Z', 'home': 'Betis', 'away': 'Levante'}, 'arguments': {'home_score': '2', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:58.403064Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.692', 'name': [['en', 'Fulham v Leeds']], 'season': [['en', '']], 'start_time': '2021-03-19T20:00:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'upcoming', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-19T20:00:00Z', 'home': 'Fulham', 'away': 'Leeds'}, 'arguments': {'home_score': '1', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:58.405637Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.691', 'name': [['en', 'Fulham v Leeds']], 'season': [['en', '']], 'start_time': '2021-03-19T20:00:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'in_progress', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-19T20:00:00Z', 'home': 'Fulham', 'away': 'Leeds'}, 'arguments': {'home_score': '1', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:58.409635Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.720', 'name': [['en', 'Ath Bilbao v Eibar']], 'season': [['en', '']], 'start_time': '2021-03-20T13:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-20T13:00:00Z', 'home': 'Ath Bilbao', 'away': 'Eibar'}, 'arguments': {'home_score': '1', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:58.460529Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.721', 'name': [['en', 'Ath Bilbao v Eibar']], 'season': [['en', '']], 'start_time': '2021-03-20T13:00:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'upcoming', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-20T13:00:00Z', 'home': 'Ath Bilbao', 'away': 'Eibar'}, 'arguments': {'home_score': '1', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:58.507307Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.731', 'name': [['en', 'Crotone v Bologna']], 'season': [['en', '']], 'start_time': '2021-03-20T14:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-20T14:00:00Z', 'home': 'Crotone', 'away': 'Bologna'}, 'arguments': {'home_score': '2', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:58.566822Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.762', 'name': [['en', 'Werder Bremen v Wolfsburg']], 'season': [['en', '']], 'start_time': '2021-03-20T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-20T14:30:00Z', 'home': 'Werder Bremen', 'away': 'Wolfsburg'}, 'arguments': {'home_score': '1', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:58.630686Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.678', 'name': [['en', 'Ein Frankfurt v Union Berlin']], 'season': [['en', '']], 'start_time': '2021-03-20T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-20T14:30:00Z', 'home': 'Ein Frankfurt', 'away': 'Union Berlin'}, 'arguments': {'home_score': '5', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:58.768115Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.677', 'name': [['en', 'Bayern Munich v Stuttgart']], 'season': [['en', '']], 'start_time': '2021-03-20T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-20T14:30:00Z', 'home': 'Bayern Munich', 'away': 'Stuttgart'}, 'arguments': {'home_score': '4', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:58.84996Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.738', 'name': [['en', 'FC Koln v Dortmund']], 'season': [['en', '']], 'start_time': '2021-03-20T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-20T14:30:00Z', 'home': 'FC Koln', 'away': 'Dortmund'}, 'arguments': {'home_score': '2', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:58.917591Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.676', 'name': [['en', 'Bayern Munich v Stuttgart']], 'season': [['en', '']], 'start_time': '2021-03-20T14:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-20T14:30:00Z', 'home': 'Bayern Munich', 'away': 'Stuttgart'}, 'arguments': {'home_score': '4', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:58.986362Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.758', 'name': [['en', 'Celta Vigo v Real Madrid']], 'season': [['en', '']], 'start_time': '2021-03-20T15:15:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-20T15:15:00Z', 'home': 'Celta Vigo', 'away': 'Real Madrid'}, 'arguments': {'home_score': '1', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:59.029494Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.733', 'name': [['en', 'Spezia v Cagliari']], 'season': [['en', '']], 'start_time': '2021-03-20T17:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'upcoming', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-20T17:00:00Z', 'home': 'Spezia', 'away': 'Cagliari'}, 'arguments': {'home_score': '2', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:59.088149Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.732', 'name': [['en', 'Spezia v Cagliari']], 'season': [['en', '']], 'start_time': '2021-03-20T17:00:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-20T17:00:00Z', 'home': 'Spezia', 'away': 'Cagliari'}, 'arguments': {'home_score': '2', 'away_score': '1'}, 'timestamp': '2021-03-29T06:47:59.143532Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.759', 'name': [['en', 'Huesca v Osasuna']], 'season': [['en', '']], 'start_time': '2021-03-20T17:30:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'in_progress', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-20T17:30:00Z', 'home': 'Huesca', 'away': 'Osasuna'}, 'arguments': {'home_score': '0', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:59.185056Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.760', 'name': [['en', 'Huesca v Osasuna']], 'season': [['en', '']], 'start_time': '2021-03-20T17:30:00', 'event_group_id': '1.21.9', 'scores': [], 'status': 'upcoming', 'event_group_name': 'LaLiga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'LaLiga', 'start_time': '2021-03-20T17:30:00Z', 'home': 'Huesca', 'away': 'Osasuna'}, 'arguments': {'home_score': '0', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:59.226237Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.736', 'name': [['en', 'Schalke 04 v Mönchengladbach']], 'season': [['en', '']], 'start_time': '2021-03-20T17:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'in_progress', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-20T17:30:00Z', 'home': 'Schalke 04', 'away': 'Mönchengladbach'}, 'arguments': {'home_score': '0', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:59.293945Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.737', 'name': [['en', 'Schalke 04 v Mönchengladbach']], 'season': [['en', '']], 'start_time': '2021-03-20T17:30:00', 'event_group_id': '1.21.23', 'scores': [], 'status': 'upcoming', 'event_group_name': 'Bundesliga', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'Bundesliga', 'start_time': '2021-03-20T17:30:00Z', 'home': 'Schalke 04', 'away': 'Mönchengladbach'}, 'arguments': {'home_score': '0', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:59.364111Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.761', 'name': [['en', 'Inter v Sassuolo']], 'season': [['en', '']], 'start_time': '2021-03-20T19:45:00', 'event_group_id': '1.21.14', 'scores': [], 'status': 'in_progress', 'event_group_name': 'SerieA', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'SerieA', 'start_time': '2021-03-20T19:45:00Z', 'home': 'Inter', 'away': 'Sassuolo'}, 'arguments': {'whistle_start_time': '2021-03-20T19:45:00Z', 'season': ''}, 'timestamp': '2021-03-29T06:47:59.419867Z', 'call': 'canceled'}}, {'eventFromChain': {'id': '1.22.693', 'name': [['en', 'Brighton v Newcastle']], 'season': [['en', '']], 'start_time': '2021-03-20T20:00:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'in_progress', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-20T20:00:00Z', 'home': 'Brighton', 'away': 'Newcastle'}, 'arguments': {'home_score': '3', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:59.42212Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.694', 'name': [['en', 'Brighton v Newcastle']], 'season': [['en', '']], 'start_time': '2021-03-20T20:00:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'upcoming', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-20T20:00:00Z', 'home': 'Brighton', 'away': 'Newcastle'}, 'arguments': {'home_score': '3', 'away_score': '0'}, 'timestamp': '2021-03-29T06:47:59.423875Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.747', 'name': [['en', 'West Ham v Arsenal']], 'season': [['en', '']], 'start_time': '2021-03-21T15:00:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'upcoming', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-21T15:00:00Z', 'home': 'West Ham', 'away': 'Arsenal'}, 'arguments': {'home_score': '3', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:59.4243Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.746', 'name': [['en', 'West Ham v Arsenal']], 'season': [['en', '']], 'start_time': '2021-03-21T15:00:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'in_progress', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-21T15:00:00Z', 'home': 'West Ham', 'away': 'Arsenal'}, 'arguments': {'home_score': '3', 'away_score': '3'}, 'timestamp': '2021-03-29T06:47:59.424729Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.745', 'name': [['en', 'Aston Villa v Tottenham']], 'season': [['en', '']], 'start_time': '2021-03-21T19:30:00', 'event_group_id': '1.21.8', 'scores': [], 'status': 'in_progress', 'event_group_name': 'EPL', 'sport': 'Soccer'}, 'eventFromFeed': {'id': {'sport': 'Soccer', 'event_group_name': 'EPL', 'start_time': '2021-03-21T19:30:00Z', 'home': 'Aston Villa', 'away': 'Tottenham'}, 'arguments': {'home_score': '0', 'away_score': '2'}, 'timestamp': '2021-03-29T06:47:59.425529Z', 'call': 'result'}}, {'eventFromChain': {'id': '1.22.772', 'name': [['en', 'Utah Jazz @ Golden State Warriors']], 'season': [['en', '']], 'start_time': '2021-03-23T10:30:00', 'event_group_id': '1.21.5', 'scores': [], 'status': 'in_progress', 'event_group_name': 'NBA Regular Season', 'sport': 'Basketball'}, 'eventFromFeed': None}, {'eventFromChain': {'id': '1.22.773', 'name': [['en', 'Denver Broncos @ Cincinnati Bengals']], 'season': [['en', '']], 'start_time': '2021-03-23T16:30:00', 'event_group_id': '1.21.16', 'scores': [], 'status': 'in_progress', 'event_group_name': 'NFL Regular Season', 'sport': 'AmericanFootball'}, 'eventFromFeed': None}]
    return newDict
 
def UpdateListVersionOne(request):
    '''
    param : request
    description : To load update page
    '''
    try:
        if index_page_permitted(request):
            params = {'filter':'events'}
            # events = getstaticEvents()
            # print(events)
            events = GetMatchingEvents()
            # print(events)
            # events = []
            # events = None
            list_values = {}
            if events is not None:
                list_values = dict(enumerate(events , start=1))
            return render(request, 'update_match_events.html',{"data": list_values})
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
    print(data)
    # result={}
    result = UpdatePotato(data)
    if(len(result) == 0) :
        return JsonResponse({'success':event + " : " + call})
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



