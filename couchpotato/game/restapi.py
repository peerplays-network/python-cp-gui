import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from couch_potato import cp_local
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
cp = cp_local.Cp()

class CreatePotatos(APIView):

    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('sport', openapi.IN_QUERY, "Enter the sports event if available", type=openapi.TYPE_STRING),
    openapi.Parameter('eventGroup', openapi.IN_QUERY, "Enter Event Group if available", type=openapi.TYPE_STRING),
    ])
    def get(self, request):
        '''
        Description : Get options to select for create
        '''
        rDict = dict()  
        sport = None
        eventGroup = None
        if request.GET.get('sport'):
            sport = request.GET["sport"]
        if request.GET.get('eventGroup'):
            eventGroup = request.GET["eventGroup"]
        try:
            rDict = cp.GetForCreate(sport,eventGroup) 
        except Exception as e:
            rDict["status"] = "error"
            rDict["error"] = str(e)
        return Response(rDict)



    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('sport', openapi.IN_QUERY, "Enter the sports event", type=openapi.TYPE_STRING),
    openapi.Parameter('eventGroup', openapi.IN_QUERY, "Enter Event Group", type=openapi.TYPE_STRING),
    openapi.Parameter('home', openapi.IN_QUERY, "Enter Home", type=openapi.TYPE_STRING),
    openapi.Parameter('away', openapi.IN_QUERY, "Enter Away", type=openapi.TYPE_STRING),
    openapi.Parameter('startTime', openapi.IN_QUERY, "Enter Date time in format 2018-03-20T09:12:28Z", type=openapi.TYPE_STRING),    
    ])
    def post(self,request):
        '''
        Description : Post your data to create
        '''
        rDict = dict()
        try:
            record = dict(request.GET)
            if "sport" not in record.keys() and "eventGroup" not in record.keys() and "home" not in record.keys() and "away" not in record.keys() and "startTime" not in record.keys():
                raise Exception("Parameter missing")
        except Exception as e:
            rDict["status"] = "error"
            rDict["error"] ="error in get params" +str(e)
        try:
            print(record["sport"],record["eventGroup"],record["home"],record["away"],record["startTime"])
            rDict = cp.CreateForApi(record["sport"],record["eventGroup"],record["home"],record["away"],record["startTime"])
        except Exception as e:
            rDict["status"] = "error"
            rDict["error"] = "error in get create for api"+str(e)
        return Response(rDict)
        


class UpdatePotatos(APIView):
       
        def get(self, request):
            '''
            Description : Get all list to update
            '''
            rDict = dict()
            try:
                rDict = cp.EventsAllSortedForApi()
            except Exception as e:
                rDict["status"] = "error"
                rDict["error"] = str(e)
            return Response(rDict)


        @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('event', openapi.IN_QUERY, "Enter the sports event", type=openapi.TYPE_OBJECT),
        openapi.Parameter('call', openapi.IN_QUERY, "Enter options like in_progress , finish , result , canceled", type=openapi.TYPE_STRING),
        openapi.Parameter('homeScore', openapi.IN_QUERY, "Enter Home Score if call is `finish`", type=openapi.TYPE_NUMBER,format=openapi.FORMAT_DOUBLE),
        openapi.Parameter('awayScore', openapi.IN_QUERY, "Enter Away Score if call is `finish`", type=openapi.TYPE_NUMBER,format=openapi.FORMAT_DOUBLE),
        ])
        def post(self,request):
            '''
            Description : Post Details for Update
            '''
            rDict = {}
            try:
                homeScore = None
                awayScore = None
                record = request.GET
                print(record)
                if "event" not in record.keys():
                    raise Exception("Events is mandatory")
                if "event" not in record.keys():
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
                # print("Event " , event , call , homeScore, awayScore)
                cp.UpdateForApi(self, event, call, homeScore=None, awayScore=None)
            except Exception as e:
                rDict["status"] = "error"
                rDict["error"] =str(e)
            return Response(rDict)
 
