# # Create your views here.
# from django.http import Http404 , JsonResponse
# from django.shortcuts import render
# import json
# import requests
# import pytz, datetime
 
# def AutoCreateCouchPotato(request):
     
#     create_value=dict()

#     games =  requests.get('https://www.thesportsdb.com/api/v1/json/1/all_leagues.php')
#     json_data = games.json()
#     league = json_data['leagues']
#     res = next((l for l in league if l['strLeague'] == 'NFL'), None)

#     print(res['idLeague'])
#     create_value['league'] = res['strLeague']
#     create_value['idleague'] = res['idLeague']

#     season =  requests.get('https://www.thesportsdb.com/api/v1/json/1/search_all_seasons.php?id='+create_value['idleague'])
#     json_season = season.json()['seasons'][-1]
#     print(json_season)
#     create_value['season'] = json_season['strSeason']

#     comming_events = requests.get('https://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id='+create_value['idleague'])
#     json_events = comming_events.json()['events']
#     print(json_events)

#     create_value['comming_events'] = json_events


#     return JsonResponse( create_value)
    


# def post_create(request):
#     question_id = request.POST.get("id")
#     option_text = request.POST.get("optiontext")
#     question_id = int(question_id)
#     if question_id == 1:
#         request.session['sport'] = option_text
#     elif question_id == 2:
#         request.session['eventGroup'] = option_text
#     elif question_id == 3:
#         request.session['home'] = option_text
#     elif question_id == 4:
#         request.session['away'] = option_text
#     elif question_id == 5:
#         request.session['startTime'] = option_text
#         data = {"sport":request.session['sport'].strip() ,"eventGroup":request.session['eventGroup'].strip(),"home":request.session['home'].strip(),"away":request.session['away'].strip(),"startTime":request.session['startTime'].strip()}
#         print("Data " , data)
#         result = requests.post('http://s3.jemshid.com:8000/sports/api/game/', data = data)
#         if(len(eval(result.text)) > 0):
#             return JsonResponse({'success':'Posted','message':result.text})
#         else:
#             JsonResponse({'success':'Error','message':result.text})
#     return JsonResponse({'success':True,'message':'success'})
