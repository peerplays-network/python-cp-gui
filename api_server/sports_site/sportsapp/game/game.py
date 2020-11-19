import sys

from rest_framework.views import APIView
from rest_framework.response import Response
#sys.path.insert(0,"../../")
from couch_potato import cp_local
#from python_cp.cp_local import Cp

class Game(APIView):
	def get(self, request, format=None):
                rDict = dict()
                sport = None
                eventGroup = None
                cp = cp_local.Cp()
                if request.GET.get('sport'):
                    sport = request.GET["sport"]
                if request.GET.get('eventGroup'):
                    eventGroup = request.GET["eventGroup"]
                if request.GET.get("filter"):
                    if request.GET["filter"] == "events":
                        try:
                            rDict = cp.EventsAllSortedForApi()
                        except Exception as e:
                            rDict["status"] = "error"
                            rDict["error"] = str(e)
                        return Response(rDict)
                try:
                    print(eventGroup,sport)
                    rDict = cp.GetForCreate(sport,eventGroup) 
                except Exception as e:
                    rDict["status"] = "error"
                    rDict["error"] = str(e)
                return Response(rDict)
	def post(self,request):
            rDict = dict()
            try:
                record = request.data
                if "sport" not in record.keys() and "eventGroup" not in record.keys() and "home" not in record.keys() and "away" not in record.keys() and "startTime" not in record.keys():
                    raise Exception("Parameter missing")
            except Exception as e:
                rDict["status"] = "error"
                rDict["error"] ="errorin get params" +str(e)
            try:
                cp = cp_local.Cp()
                rDict = cp.CreateForApi(record["sport"],record["eventGroup"],record["home"],record["away"],record["startTime"])
            except Exception as e:
                rDict["status"] = "error"
                rDict["error"] = "error in get create for api"+str(e)
            return Response(rDict)
	def put(self,request):
            rDict = {}
            try:
                homeScore = None
                awayScore = None
                record = request.data
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
                return Response(rDict)
            try:
                cp = cp_local.Cp()
                cp.UpdateForApi(self, event, call, homeScore=None, awayScore=None)
            except Exception as e:
                rDict["status"] = "error"
                rDict["error"] =str(e)
            return Response(rDict)
