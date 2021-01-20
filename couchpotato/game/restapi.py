import sys
from rest_framework.views import APIView
from rest_framework.response import Response
# from couch_potato import cp_local
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import cp_local
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
    openapi.Parameter('startTime', openapi.IN_QUERY, "Enter Date time in format 2021-01-19T18:30:00.000Z", type=openapi.TYPE_STRING),    
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
        
        username = request.user.username
        if username is '':
            rDict["status"] = "error"
            rDict["error"] ="Require Authentication"

        else:
            try:
                if type(record["sport"]) == list:
                    record["sport"] = record["sport"][0].strip()
                if type(record["eventGroup"]) == list:
                    record["eventGroup"] = record["eventGroup"][0].strip()
                if type(record["home"]) == list:
                    record["home"] = record["home"][0].strip()
                if type(record["away"]) == list:
                    record["away"] = record["away"][0].strip()
                if type(record["startTime"]) == list:
                    record["startTime"] = record["startTime"][0].strip()
                rDict = cp.CreateForApiWithPotato(record["sport"],record["eventGroup"],record["home"],record["away"],record["startTime"],username)

            except Exception as e:
                rDict["status"] = "error"
                rDict["error"] = "error in create for api : "+str(e)

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
            username = request.user.username
           

            if username is '':
                rDict["status"] = "error"
                rDict["error"] ="Require Authentication"

            else:
                try:
                    homeScore = None
                    awayScore = None
                    event = dict()
                    record = request.GET
                    if "event" not in record.keys():
                        raise Exception("Events is mandatory")
                    if "event" not in record.keys():
                        raise Exception('call is manadatory')
                    
                    if type(record["event"]) == str:
                        event = eval(record["event"])
                    if type(record["call"]) == list:
                        record["call"] = record["call"][0]

                    if "homeScore" in record.keys():
                        homeScore = record["homeScore"]
                    if "awayScore" in record.keys():
                        awayScore = record["awayScore"]
            
                except Exception as e:
                    rDict["status"] = "error"
                    rDict["error"] = str(e)
                    return Response(rDict)

                try:
                    cp.UpdateForApiWithPotato(event, record["call"], username,homeScore, awayScore)
                    rDict["status"] = "Success"

                except Exception as e:
                    rDict["status"] = "error in update potato"
                    rDict["error"] =str(e)
            
            return Response(rDict)
 
