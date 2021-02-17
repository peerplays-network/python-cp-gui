from django.shortcuts import render
# from couch_potato import cp_local
from django.http import Http404 , JsonResponse

# Create your views here.
import cp_local
cp = cp_local.Cp()

def GetEvents(params={}):
    rDict = dict()
    sport = None
    eventGroup = None
    if 'sport' in params:
        sport = params["sport"]
    if 'eventGroup' in params:
        eventGroup = params["eventGroup"]
    if 'filter' in params:
        if params["filter"] == "events":
            try:
                rDict = cp.EventsAllSortedForApi()
                # rDict = cp.EventsAllWithEventGroupName(rDict)
            except Exception as e:
                rDict["status"] = "error"
                rDict["error"] = str(e)
            return rDict
    try:
        print(eventGroup, sport)
        rDict = cp.GetForCreate(sport, eventGroup)
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] = str(e)
    return rDict


def Create(record):
    rDict = dict()
    try:
        if "sport" not in record.keys() and "eventGroup" not in record.keys() and "home" not in record.keys() and "away" not in record.keys() and "startTime" not in record.keys():
            raise Exception("Parameter missing")
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] ="errorin get params" +str(e)
    try:
        rDict = cp.CreateForApi(record["sport"],record["eventGroup"],record["home"],record["away"],record["startTime"])
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] = "error in get create for api"+str(e)
    return rDict


def CreatePotato(record):
    rDict = dict()
    try:
        if "sport" not in record.keys() and "eventGroup" not in record.keys() and "home" not in record.keys() and "away" not in record.keys() and "startTime" not in record.keys():
            raise Exception("Parameter missing")
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] ="errorin get params" +str(e)
    try:
        rDict = cp.CreateForApiWithPotato(record["sport"],record["eventGroup"],record["home"],record["away"],record["startTime"],record['username'])
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] = "error in get create for api"+str(e)
    return rDict

def Update(record):
    print('in Update')
    rDict = {}
    try:
        homeScore = None
        awayScore = None
        if "event" not in record.keys():
            raise Exception("Events is mandatory")
        if "call" not in record.keys():
            raise Exception('call is manadatory')
        event = record["event"]
        call = record["call"]
        if "homeScore" in record.keys():
            homeScore = record["homeScore"]
        if "awayScore" in record.keys():
            awayScore = record["awayScore"]
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] = str(e)
        return rDict
    try:
        cp.UpdateForApi(event, call, homeScore, awayScore)
    except Exception as e:
        rDict["status"] = "Error at game/view/Update line 88"
        rDict["error"] =str(e)
        print(e)
    return rDict





def UpdatePotato(record):
    print("in UpdatePotato")
    rDict = {}
    try:
        homeScore = None
        awayScore = None
        if "event" not in record.keys():
            raise Exception("Events is mandatory")
        if "call" not in record.keys():
            raise Exception('call is manadatory')
        event = record["event"]
        call = record["call"]
        potatouser = record["username"]
        if "homeScore" in record.keys():
            homeScore = record["homeScore"]
        if "awayScore" in record.keys():
            awayScore = record["awayScore"]
    except Exception as e:
        rDict["status"] = "Error at game/view/UpdatePotato line 114"
        rDict["error"] = str(e)
        print(rDict)
        print(e)
        return rDict
#    try:
#        print("Event > " ,record["event"] , '\n Type ', type(record["event"]))
#        print("Call ", record["call"])
#        print("username " , potatouser)
#        print("homeScore " , homeScore)
#        print("awayScore " , awayScore)

    cp.UpdateForApiWithPotato(event, call, potatouser,homeScore, awayScore)
#    except Exception as e:
#        rDict["status"] = "Error at game/view/UpdatePotato line 127"
#        rDict["error"] =str(e)
#        print(rDict)
#        print(e)
    return rDict
