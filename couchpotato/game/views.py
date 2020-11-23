from django.shortcuts import render
from couch_potato import cp_local
from django.http import Http404 , JsonResponse

# Create your views here.
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
            except Exception as e:
                rDict["status"] = "error"
                rDict["error"] = str(e)
            return rDict
    try:
        print(eventGroup,sport)
        rDict = cp.GetForCreate(sport,eventGroup) 
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] = str(e)
    return rDict

def Create(record):
    rDict = dict()
    try:
        # record = request.data
        if "sport" not in record.keys() and "eventGroup" not in record.keys() and "home" not in record.keys() and "away" not in record.keys() and "startTime" not in record.keys():
            raise Exception("Parameter missing")
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] ="errorin get params" +str(e)
    try:
        # cp = cp_local.Cp()
        rDict = cp.CreateForApi(record["sport"],record["eventGroup"],record["home"],record["away"],record["startTime"])
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] = "error in get create for api"+str(e)
    return rDict


def Update(record):
    rDict = {}
    try:
        homeScore = None
        awayScore = None
        # record = request.data
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
        # cp = cp_local.Cp()
        cp.UpdateForApi(event, call, homeScore, awayScore)
    except Exception as e:
        rDict["status"] = "error"
        rDict["error"] =str(e)
    return rDict