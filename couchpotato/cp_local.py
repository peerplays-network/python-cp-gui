
from bos_incidents import factory, exceptions
import _thread
import time
import numpy as np
import pandas as pd
from bos_mint.node import Node
from bookiesports.normalize import IncidentsNormalizer
from bookiesports import BookieSports
from bos_incidents.format import string_to_incident, incident_to_string
from bos_incidents.datestring import date_to_string, string_to_date
from datetime import datetime, timezone
import requests
import yaml
import logging

with open("config-bos-mint.yaml", "r") as f:
    config = yaml.safe_load(f)
chainName = config["connection"]["use"]
bosApis = config["bosApis"]
potatoNames = config["potatoNames"]

# Create and configure logger
# logging.basicConfig(filename="za.log",
#                     format='%(asctime)s %(message)s',
#                     filemode='a')
# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

node = Node()
# node.unlock("peerplays**")
# node.unlock(config["password"])
ppy = node.get_node()
rpc = ppy.rpc

INCIDENT_CALLS = [
    "create",
    "in_progress",
    "finish",
    "result",
    "canceled",
    "dynamic_bmgs",
]

STATUSES = ["upcoming", "in_progress", "finished"]

# normalizer = IncidentsNormalizer(chain="elizabeth")
normalizer = IncidentsNormalizer(chain=chainName)
normalize = normalizer.normalize

# Incident Storage
storage = factory.get_incident_storage()


def substitution(teams, scheme):
    class Teams:
        home = " ".join([x for x in teams[0].split(" ")])
        away = " ".join([x for x in teams[1].split(" ")])

    ret = dict()
    for lang, name in scheme.items():
        ret[lang] = name.format(teams=Teams)
    ret = ret["en"]
    return ret


class Cp():

    def __init__(self):
        self.maxOpenProposals = 2
        self.delayBetweenBosPushes = 1  # in seconds
        self.bookiesports = BookieSports(chainName)
        pass

    def GetKey(self, keys):
        keys = list(keys)
        k = 0
        for key in keys:
            print(k, key)
            k = k + 1
        index = input("Enter index of key: ")
        index = int(index)
        return keys[index]

    def GetKeyParticipant(self, keys, participantDisplays):
        keys = list(keys)
        k = 0
        for key in keys:
            # print(k, participantDisplays[k])
            print(k, key)
            k = k + 1
        index = input("Enter index of key: ")
        index = int(index)
        return keys[index]

    def GetSportsList(self):
        return list(self.bookiesports.keys())

    def GetEventGroupsList(self, sport):
        eventGroupsList = self.bookiesports[sport]["eventgroups"].keys()
        eventGroupsList = list(eventGroupsList)
        return eventGroupsList

    def GetParticipants(self, sport, participantKey):
        participants = self.bookiesports[sport]["participants"][
            participantKey]["participants"]
        particpantIdentifiers = []
        participantDisplays = []
        for participant in participants:
            # particpantIdentifiers.append(participant["aliases"][0])
            participantDisplays.append(participant.values())
            particpantIdentifiers.append(participant["identifier"])
            # particpantIdentifiers.append(participant["name"]["en"])
        return particpantIdentifiers, participantDisplays

    def GetForCreate(self, sport=None, eventGroup=None):
        if isinstance(sport, type(None)):
            self._sportsList = self.GetSportsList()
            return self._sportsList
        if isinstance(eventGroup, type(None)):
            self._eventGroupsList = self.GetEventGroupsList(sport)
            return self._eventGroupsList
#        self._eventGroupIdentifier = self.bookiesports[sport][
#                "eventgroups"][eventGroup]["identifier"]
        self._participantKey = self.bookiesports[sport]["eventgroups"][
            eventGroup]["participants"]
        self._participants, participantDisplays = self.GetParticipants(
            sport, self._participantKey)
        return self._participants

    def CreateForApi(self, sport, eventGroup, home, away, startTime):
        incident = dict()
        incident["call"] = INCIDENT_CALLS[0]

        incident["id"] = dict()
        incident["id"]["sport"] = sport
        eventGroupIdentifier = self.bookiesports[sport][
            "eventgroups"][eventGroup]["identifier"]
        incident["id"]["event_group_name"] = eventGroupIdentifier
        # incident["id"]["event_group_name"] = self._eventGroup
        startTime = date_to_string(startTime)
        incident["id"]["start_time"] = startTime
        incident["arguments"] = {"whistle_start_time": startTime}
        incident["id"]["home"] = home
        incident["id"]["away"] = away
        incident["timestamp"] = date_to_string(datetime.now(tz=timezone.utc))
        incident["arguments"]["season"] = ""

        rs = []
        for potatoName in potatoNames:
            r = self.Push2bos(incident, potatoName)
            rs.append(r)
        return incident, rs

    def CreateForApiWithPotato(
            self, sport, eventGroup, home, away, startTime, potato):
        incident = dict()
        incident["call"] = INCIDENT_CALLS[0]

        incident["id"] = dict()
        incident["id"]["sport"] = sport
        eventGroupIdentifier = self.bookiesports[sport][
            "eventgroups"][eventGroup]["identifier"]
        incident["id"]["event_group_name"] = eventGroupIdentifier
        # incident["id"]["event_group_name"] = self._eventGroup
        startTime = date_to_string(startTime)
        incident["id"]["start_time"] = startTime
        incident["arguments"] = {"whistle_start_time": startTime}
        incident["id"]["home"] = home
        incident["id"]["away"] = away
        incident["timestamp"] = date_to_string(datetime.now(tz=timezone.utc))
        incident["arguments"]["season"] = ""

        self.Push2bos(incident, potato)
        return incident

    def CliManufactureCreateIncident(self):
        self._call = INCIDENT_CALLS[0]
        self._sportsList = self.GetSportsList()
        print("")
        print("Select Sport")
        self._sport = self.GetKey(self._sportsList)
        # self._sport = self.bookiesports[self._sport]["aliases"][0]
        self._eventGroupsList = self.GetEventGroupsList(self._sport)
        print("")
        print("Select Event Group")
        self._eventGroup = self.GetKey(self._eventGroupsList)
        self._eventGroupIdentifier = self.bookiesports[self._sport][
            "eventgroups"][self._eventGroup]["identifier"]
        # self._eventGroupIdentifier = self.bookiesports[self._sport][
        # "eventgroups"][self._eventGroup]["aliases"][0]
        self._participantKey = self.bookiesports[self._sport]["eventgroups"][
                self._eventGroup]["participants"]
        self._participants, participantDisplays = self.GetParticipants(
            self._sport, self._participantKey)
        print("")
        print("Select Home Team")
        self._home = self.GetKeyParticipant(
                self._participants, participantDisplays)
        print("")
        print("Select Away Team")
        self._away = self.GetKeyParticipant(
                self._participants, participantDisplays)

        incident = dict()
        incident["call"] = self._call

        # incident["arguments"] = {
        # "whistle_start_time": "2020-08-25T22:22:45.00Z"}
        incident["id"] = dict()
        incident["id"]["sport"] = self._sport
        incident["id"]["event_group_name"] = self._eventGroupIdentifier
        # incident["id"]["event_group_name"] = self._eventGroup
        print("")
        startTime = input(
                "Enter Start Time in the format 2020-08-25T22:00:00Z :")
        startTime = date_to_string(startTime)
        incident["id"]["start_time"] = startTime
        incident["arguments"] = {"whistle_start_time": startTime}
        # incident["id"]["start_time"] = "2020-08-25T22:00:00Z"
        incident["id"]["home"] = self._home
        incident["id"]["away"] = self._away
        incident["timestamp"] = date_to_string(datetime.now(tz=timezone.utc))
        incident["arguments"]["season"] = ""

        # string = incident_to_string(incident)

        return incident

    def EventsAllSorted(self):
        print('Fetching all active events, wait a few seconds')
        eventsAll = node.getEvents("all")
        eventsAll = pd.DataFrame(eventsAll)
        if len(eventsAll) == 0:
            return None
        eventsAll = eventsAll.sort_values("start_time")
        return eventsAll

    def EventsAllSortedForApi(self):
        print('Fetching all active events, wait a few seconds')
        try:
            eventsAllRaw = node.getEvents("all")
            self.eventsAllRaw = eventsAllRaw
        except Exception as e:
            logger.info(e)
            eventsAllRaw = self.eventsAllRaw
        eventsAll = pd.DataFrame(eventsAllRaw)
        if len(eventsAll) == 0:
            return None
        eventsAll = eventsAll.sort_values("start_time")
        eventsAllList = []
        for k in range(len(eventsAll)):
            eventsAllList.append(dict(eventsAll.iloc[k]))
        eventsAllList = self.EventsAllWithEventGroupName(eventsAllList)
        return eventsAllList

    def EventsAllWithEventGroupName(self, eventsAll):
        for event in eventsAll:
            event_group_id = event["event_group_id"]
            # event["event_group_name"] = rpc.get_object(
            # event_group_id)["name"][1][1]
            eventGroup = rpc.get_object(event_group_id)

            event["event_group_name"] = dict(eventGroup["name"])["identifier"]
            # event["event_group_name"] = eventGroup["name"][1][1]
            sport = rpc.get_object(eventGroup["sport_id"])
            sport = dict(sport["name"])["identifier"]
            event["sport"] = sport
            # sport = normalizer._get_sport_identifier(sport, True)
        return eventsAll

    def Event2Update(self):
        eventsAll = self.EventsAllSorted()
        if isinstance(eventsAll, type(None)):
            return None
        self._eventsAll = eventsAll
        for k in range(len(eventsAll)):
            event = eventsAll.iloc[k]
            print("")
            print(event)
            eventGroup = node.getEventGroup(event["event_group_id"])
            print(eventGroup["name"])
            sport = node.getSport(eventGroup["sport_id"])
            print(sport)
            choice = input(
                    "'U'pdate the event/'S'kip to the next event, u/s : ")
            if choice == "u":
                return event
            else:
                k = k + 1
        return None

    def HomeAway(self, homeAway):
        try:
            home, away = homeAway.split(" @ ")
        except ValueError:
            home, away = homeAway.split(" v ")
        return home, away

    def EventGroupAlias(self, sport, eventGroup):
        bookieEventGroups = self.bookiesports[sport]["eventgroups"]
        keys = list(bookieEventGroups.keys())
        for key in keys:
            if eventGroup == bookieEventGroups[key]["identifier"]:
                return bookieEventGroups[key]["aliases"][0]
        print("eventGroup Identifier NOT found: ", sport, eventGroup)

    def EventScheme(self, sport, eventGroup):
        sports = self.bookiesports[sport]
        eventGroups = sports["eventgroups"]
        for eg in eventGroups:
            if eventGroups[eg]["identifier"] == eventGroup:
                eventScheme = eventGroups[eg]
        eventScheme = eventScheme["eventscheme"]["name"]
        return eventScheme

    def UpdateForApi(self, event, call, homeScore=None, awayScore=None):
        self._event = event
        self._call = call
        incident = dict()
        incident["call"] = self._call

        startTime = event["start_time"] + "Z"
        self._starttime = startTime
        incident["id"] = dict()
        eventGroup = rpc.get_object(event["event_group_id"])

        sport = rpc.get_object(eventGroup["sport_id"])

        eventGroup = dict(eventGroup["name"])["identifier"]
        sport = dict(sport["name"])["identifier"]
        sport = normalizer._get_sport_identifier(sport, True)
        self._sport = sport
        sportAlias = self.bookiesports[sport]["aliases"][0]

        print(sport, eventGroup, startTime)

        eventGroup = normalizer._get_eventgroup_identifier(
                sport,
                eventGroup,
                startTime,
                True)

        self._eventGroup = eventGroup
        # eventGroupAlias = self.EventGroupAlias(sport, eventGroup)
        # eventGroupAlias = self.bookiesports[sport]["eventgroups"][
        # eventGroup]["aliases"][0]

        homeAway = event["name"][0][1]
        self._homeAway = homeAway
        home, away = self.HomeAway(homeAway)
        eventScheme = self.EventScheme(sport, eventGroup)
        homeAway = substitution([home, away], eventScheme)
        home, away = self.HomeAway(homeAway)

        homeAlias = normalizer._get_participant_identifier(
                sport,
                eventGroup,
                home,
                True)

        awayAlias = normalizer._get_participant_identifier(
                sport,
                eventGroup,
                away,
                True)

        # incident["id"]["event_group_name"] = eventGroupAlias
        incident["id"]["event_group_name"] = eventGroup

        incident["id"]["sport"] = sportAlias

        incident["id"]["start_time"] = startTime
        incident["arguments"] = {"whistle_start_time": startTime}
        # incident["id"]["start_time"] = "2020-08-25T22:00:00Z"

        incident["id"]["home"] = homeAlias
        incident["id"]["away"] = awayAlias
        incident["timestamp"] = date_to_string(datetime.now(tz=timezone.utc))
        incident["arguments"]["season"] = event["season"][0][1]

        if self._call == "result":
            incident["arguments"]["home_score"] = homeScore
            incident["arguments"]["away_score"] = awayScore

        self._incident = incident
        # string = incident_to_string(incident)

        rs = []
        for potatoName in potatoNames:
            r = self.Push2bos(incident, potatoName)
            rs.append(r)
        return incident, rs

    def UpdateForApiWithPotato(
            self, event, call, potato, homeScore=None, awayScore=None):
        self._event = event
        self._call = call
        incident = dict()
        incident["call"] = self._call

        startTime = event["start_time"] + "Z"
        self._starttime = startTime
        incident["id"] = dict()
        eventGroup = rpc.get_object(event["event_group_id"])

        sport = rpc.get_object(eventGroup["sport_id"])

        eventGroup = dict(eventGroup["name"])["identifier"]
        sport = dict(sport["name"])["identifier"]
        sport = normalizer._get_sport_identifier(sport, True)
        self._sport = sport
        sportAlias = self.bookiesports[sport]["aliases"][0]

        eventGroup = normalizer._get_eventgroup_identifier(
                sport,
                eventGroup,
                startTime,
                True)

        self._eventGroup = eventGroup
        # eventGroupAlias = self.EventGroupAlias(sport, eventGroup)
        # eventGroupAlias = self.bookiesports[sport]["eventgroups"][
        # eventGroup]["aliases"][0]

        homeAway = event["name"][0][1]
        self._homeAway = homeAway
        home, away = self.HomeAway(homeAway)
        eventScheme = self.EventScheme(sport, eventGroup)
        homeAway = substitution([home, away], eventScheme)
        home, away = self.HomeAway(homeAway)

        homeAlias = normalizer._get_participant_identifier(
                sport,
                eventGroup,
                home,
                True)

        awayAlias = normalizer._get_participant_identifier(
                sport,
                eventGroup,
                away,
                True)

        # incident["id"]["event_group_name"] = eventGroupAlias
        incident["id"]["event_group_name"] = eventGroup

        incident["id"]["sport"] = sportAlias

        incident["id"]["start_time"] = startTime
        incident["arguments"] = {"whistle_start_time": startTime}
        # incident["id"]["start_time"] = "2020-08-25T22:00:00Z"

        incident["id"]["home"] = homeAlias
        incident["id"]["away"] = awayAlias
        incident["timestamp"] = date_to_string(datetime.now(tz=timezone.utc))
        incident["arguments"]["season"] = event["season"][0][1]

        if self._call == "result":
            incident["arguments"]["home_score"] = homeScore
            incident["arguments"]["away_score"] = awayScore

        self._incident = incident
        # string = incident_to_string(incident)

        self.Push2bos(incident, potato)
        return incident

    def CliUpdate(self):
        event = self.Event2Update()
        if isinstance(event, type(None)):
            return None
        self._event = event
        print("")
        print("Select Call")
        self._call = self.GetKey(INCIDENT_CALLS[1:-1])
        incident = dict()
        incident["call"] = self._call

        # incident["arguments"] = {
        # "whistle_start_time": "2020-08-25T22:22:45.00Z"}
        startTime = event["start_time"] + "Z"
        self._starttime = startTime
        incident["id"] = dict()
        eventGroup = rpc.get_object(event["event_group_id"])

        sport = rpc.get_object(eventGroup["sport_id"])

        # eventGroup = dict(eventGroup["name"])["identifier"]
        eventGroup = dict(eventGroup["name"])["identifier"]
        # sport = dict(sport["name"])["identifier"]
        sport = dict(sport["name"])["identifier"]
        sport = normalizer._get_sport_identifier(sport, True)
        self._sport = sport
        sportAlias = self.bookiesports[sport]["aliases"][0]

        eventGroup = normalizer._get_eventgroup_identifier(
                sport,
                eventGroup,
                startTime,
                True)

        self._eventGroup = eventGroup
        # eventGroupAlias = self.EventGroupAlias(sport, eventGroup)
        # eventGroupAlias = self.bookiesports[sport]["eventgroups"][
        # eventGroup]["aliases"][0]

        homeAway = event["name"][0][1]
        self._homeAway = homeAway
        home, away = self.HomeAway(homeAway)
        eventScheme = self.EventScheme(sport, eventGroup)
        homeAway = substitution([home, away], eventScheme)
        home, away = self.HomeAway(homeAway)

        homeAlias = normalizer._get_participant_identifier(
                sport,
                eventGroup,
                home,
                True)

        awayAlias = normalizer._get_participant_identifier(
                sport,
                eventGroup,
                away,
                True)

        # incident["id"]["event_group_name"] = eventGroupAlias
        incident["id"]["event_group_name"] = eventGroup

        incident["id"]["sport"] = sportAlias

        incident["id"]["start_time"] = startTime
        incident["arguments"] = {"whistle_start_time": startTime}
        # incident["id"]["start_time"] = "2020-08-25T22:00:00Z"

        incident["id"]["home"] = homeAlias
        incident["id"]["away"] = awayAlias
        incident["timestamp"] = date_to_string(datetime.now(tz=timezone.utc))
        incident["arguments"]["season"] = event["season"][0][1]

        if self._call == "result":
            print("")
            homeScore = input("Enter Home " + homeAlias + " Score: ")
            print("")
            awayScore = input("Enter Away " + awayAlias + " Score: ")
            incident["arguments"]["home_score"] = homeScore
            incident["arguments"]["away_score"] = awayScore

        self._incident = incident
        # string = incident_to_string(incident)

        return incident

    def EventFromChain(self, event):
        # event = self.Event2Update()
        if isinstance(event, type(None)):
            return None
        self._event = event
        incident = dict()

        # incident["arguments"] = {
        # "whistle_start_time": "2020-08-25T22:22:45.00Z"}
        startTime = event["start_time"] + "Z"
        self._starttime = startTime
        incident["id"] = dict()
        eventGroup = rpc.get_object(event["event_group_id"])

        sport = rpc.get_object(eventGroup["sport_id"])

        # eventGroup = dict(eventGroup["name"])["identifier"]
        eventGroup = dict(eventGroup["name"])["identifier"]
        # sport = dict(sport["name"])["identifier"]
        sport = dict(sport["name"])["identifier"]
        sport = normalizer._get_sport_identifier(sport, True)
        self._sport = sport
        sportAlias = self.bookiesports[sport]["aliases"][0]

        eventGroup = normalizer._get_eventgroup_identifier(
                sport,
                eventGroup,
                startTime,
                True)

        self._eventGroup = eventGroup
        # eventGroupAlias = self.EventGroupAlias(sport, eventGroup)
        # eventGroupAlias = self.bookiesports[sport]["eventgroups"][
        # eventGroup]["aliases"][0]

        homeAway = event["name"][0][1]
        self._homeAway = homeAway
        home, away = self.HomeAway(homeAway)
        eventScheme = self.EventScheme(sport, eventGroup)
        homeAway = substitution([home, away], eventScheme)
        home, away = self.HomeAway(homeAway)

        homeAlias = normalizer._get_participant_identifier(
                sport,
                eventGroup,
                home,
                True)

        awayAlias = normalizer._get_participant_identifier(
                sport,
                eventGroup,
                away,
                True)

        # incident["id"]["event_group_name"] = eventGroupAlias
        incident["id"]["event_group_name"] = eventGroup

        incident["id"]["sport"] = sportAlias

        incident["id"]["start_time"] = startTime
        incident["arguments"] = {"whistle_start_time": startTime}
        # incident["id"]["start_time"] = "2020-08-25T22:00:00Z"

        incident["id"]["home"] = homeAlias
        incident["id"]["away"] = awayAlias
        incident["timestamp"] = date_to_string(datetime.now(tz=timezone.utc))
        incident["arguments"]["season"] = event["season"][0][1]

        self._incident = incident
        # string = incident_to_string(incident)

        return incident

    def Update(self):
        incident = self.CliUpdate()
        if isinstance(incident, type(None)):
            print("No incident to update")
            return None, None
        rs = []
        for potatoName in potatoNames:
            r = self.Push2bos(incident, potatoName)
            rs.append(r)
        return rs
        # r = self.Push2dp(incident)

    def Push2dp(self, incident):
        self._incident = incident
        string = incident_to_string(incident)
        self._string = string
        # normalize(string_to_incident(string), True)
        params = dict()
        params["manufacture"] = string
        params["restrict_witness_group"] = "elizabeth"
        params["token"] = "pbsabookie"
        self._params = params
        # r = requests.get(url=dps["local"], params=params)
        # return r

    def Push2bos(self, incident, providerName):
        _thread.start_new_thread(self.Push2bosMethod, (incident, providerName))
        print("thread started")

    def Push2bosMethod(self, incident, providerName):
        string = incident_to_string(incident)
        self._string = string
        incident["unique_string"] = string
        incident["provider_info"] = dict()
        incident["provider_info"]["name"] = providerName
        incident["provider_info"]["pushed"] = date_to_string(
                datetime.now(tz=timezone.utc))
        self._incident = incident
        incident = normalize(incident, True)
        self._incident = incident
        logger.info(str(incident))

        while True:
            proposalsOpen = rpc.get_proposed_transactions("1.2.1")
            print("Len proposalsOpen: ",
                  len(proposalsOpen), " / ", self.maxOpenProposals)
            if len(proposalsOpen) <= self.maxOpenProposals:
                break
            else:
                time.sleep(60)

        # r = requests.post(url=bos["local"], json=incident)
        rng = np.random.default_rng()
        lBosApis = len(bosApis)
        ks = rng.choice(lBosApis, size=lBosApis, replace=False)
        # print(incident)
        for k in ks:
            # for api in bosApis:
            print("inthread:", k)
            api = list(bosApis[k].keys())[0]
            acceptedProviderNames = list(bosApis[k].values())[0]
            # print(api)
            try:
                if providerName in acceptedProviderNames:
                    print("providername in acepted list:", providerName)
                    requests.post(url=api, json=incident)
                else:
                    print("providername NOT in acepted list:", providerName)
            except Exception as e:
                print(e)
                logger.warning(api + ": failed")
            time.sleep(self.delayBetweenBosPushes)
        try:
            # FIXME, remove copy()
            storage.insert_incident(incident.copy())
        except exceptions.DuplicateIncidentException as e:
            print(e)
            # We merely pass here since we have the incident already
            # alerting anyone won't do anything
            # traceback.print_exc()
            pass

        print("thread finished")
        return

    def OpenProposalsCount(self):
        openProposalsCount = len(rpc.get_proposed_transactions("1.2.1"))
        return openProposalsCount, self.maxOpenProposals

    def History(self, providerName):
        collection = storage._get_collection(collection_name="incident")
        historyGen = collection.find({"provider_info.name": {
            "$eq": providerName}})

        history = []
        for doc in historyGen:
            history.append(doc)
        history = history[::-1]
        return history

    def Push2bosBetter(self, incident, providerNames):
        string = incident_to_string(incident)
        self._string = string
        incident["unique_string"] = string
        incident["provider_info"] = dict()
        incident["provider_info"]["pushed"] = date_to_string(
                datetime.now(tz=timezone.utc))
        self._incident = incident
        incident = normalize(incident, True)
        self._incident = incident
        logger.info(str(incident))

        # r = requests.post(url=bos["local"], json=incident)
        rng = np.random.default_rng()
        lBosApis = len(bosApis)
        ks = rng.choice(lBosApis, size=lBosApis, replace=False)
        # print(incident)
        for k in ks:
            # for api in bosApis:
            print("inthread:", k)
            api = bosApis[k]
            for providerName in providerNames:
                incident["provider_info"]["name"] = providerName
                # print(api)
                try:
                    requests.post(url=api, json=incident)
                except Exception as e:
                    print(e)
                    logger.warning(api + ": failed")
                time.sleep(self.delayBetweenBosPushes)
        print("thread finished")
        return

    def Push2bosAll(self, incident):
        self.Push2bosBetter(incident, config["potatoNames"])
        # for potato in config["potatoNames"]:
        # self.Push2bosMethod(incident, potato)

    def Create(self):
        incident = self.CliManufactureCreateIncident()
        rs = []
        for potatoName in potatoNames:
            r = self.Push2bos(incident, potatoName)
            rs.append(r)
        # r = self.Push2bos(incident, "jemshid1")
        # r2 = self.Push2bos(incident, "jemshid2")
        # r = self.Push2dp(self._incident)
        # return r, r2
        return rs

    def Choose(self):
        # print("Choose u or c:")
        print("u: Update event")
        print("c: Create event")
        choice = input("Enter your choice u/c: ")
        if choice == "u":
            self.Update()
        elif choice == "c":
            self.Create()
        else:
            print("You didn't make a relevant choice, try again")


if __name__ == "__main__":
    cp = Cp()
    # self.Choose()
    # self.Create()
    # incident = self.CliManufactureIncident()
    string_to_incident
    string_to_date
