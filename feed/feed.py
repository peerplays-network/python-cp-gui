import yaml
from dateutil.parser import parse
import requests
from bos_incidents.datestring import date_to_string, string_to_date
from datetime import datetime, timezone
import json
# import pandas as pd
from cp_local import Cp, rpc, config
import _thread
import time

leagueIds = [4328, 4391, 4387, 4380, 4424, 4335, 4332, 4331]
# 4380 : NHL # Ice Hockey
# 4424 : MLB # Baseball
# 4328 : EPL
# 4391 : NFL
# 4387 : NBA
# 4335 : LaLiga
# 4332 : Serie A
# 4562 : Friendly International : International Friendlies
# 4482 : FA Cup
# 4481 : UEFA Europa Lague
# 4480 : UEFA Champions League
# 4331 : Bundesliga


INCIDENT_CALLS = [
    "create",  # 0
    "in_progress",  # 1
    "finish",  # 2
    "result",  # 3
    "canceled",  # 4
    "dynamic_bmgs",  # 5
]

# https://www.thesportsdb.com/api/v1/json/1/eventspastleague.php?id=4391
# apiBase = "https://www.thesportsdb.com/api/v1/json/1/"
apiBase = "https://www.thesportsdb.com/api/v1/json/"
apiBase = apiBase + str(config["token"][0]) + "/"
apiEventsNextLeague = "eventsnextleague.php?id="
apiEventsPastLeague = "eventspastleague.php?id="
apiTeamsFromLeagueId = "lookup_all_teams.php?id="

apiAllLeagues = "all_leagues.php"


class Feed:

    def __init__(self):
        self.cp = Cp()
        self.failedEvents = []
        self.constCheckPeriod = 60 * 60 * 24  # in seconds
        self.maxOpenProposals = 1
        pass

    def Past15(self, leagueid):
        url = apiBase + apiEventsPastLeague + str(leagueid)
        schedule15 = requests.get(url)
        schedule15 = schedule15.text
        schedule15 = json.loads(schedule15)
        events = schedule15["events"]
        # return(schedule15)
        # def CreateForApi(self, sport, eventGroup, home, away, startTime):
        return events

    def Schedule15(self, leagueid):
        url = apiBase + apiEventsNextLeague + str(leagueid)
        schedule15 = requests.get(url)
        self._schedule15 = schedule15
        schedule15 = schedule15.text
        schedule15 = json.loads(schedule15)
        events = schedule15["events"]
        # return(schedule15)
        # def CreateForApi(self, sport, eventGroup, home, away, startTime):
        return events

    def Call(self, event, incident):

        startTime = string_to_date(incident["id"]["start_time"])
        now = datetime.now(timezone.utc)
        self.now = now
        self.startTime = startTime

        if (event["strPostponed"] == "yes") or (
                event["strStatus"] == "POST"):
            incident["call"] = INCIDENT_CALLS[4]
            print("Postponed Event")

        elif (
                event["strStatus"] == "FT") or (
                event["strStatus"] == "Match Finished") or (
                event["strStatus"] == "AP") or (
                event["strStatus"] == "AOT") or (
                    (now - startTime).days > 1):
            incident["call"] = INCIDENT_CALLS[3]
            incident["arguments"] = dict()
            incident["arguments"]["home_score"] = event["intHomeScore"]
            incident["arguments"]["away_score"] = event["intAwayScore"]
            print("Match Finished")

        elif (
                event["strStatus"] == "Not Started") or (
                event["strStatus"] == "NS"):
            incident["call"] = INCIDENT_CALLS[0]
            print("Not started or NS")

        elif (
                startTime - now).days >= 1 and isinstance(
                        event["strStatus"], type(None)):
            incident["call"] = INCIDENT_CALLS[0]
            print("None elif case and event created")

        elif (event["strStatus"] == "Second Half"):
            incident["call"] = INCIDENT_CALLS[1]
            print('Second Half', "to in_progress", event["strFilename"])

        else:
            self.failedEvents.append(event)
            print("Call Not Managed:")
        return incident

    def ToCp(self, event):
        sport = None
        eventGroup = None
        home = None
        away = None
        startTime = None
        # strEvent = event["strEvent"]
        # home, away = strEvent.split(" vs ")
        sport = event["strSport"]
        eventGroup = event["strLeague"]
        home = event["strHomeTeam"]
        away = event["strAwayTeam"]
        dateEvent = event["dateEvent"]
        strTime = event["strTime"]
        # if len(strTime.split(":")[0]) == 1:
        #     strTime = "0" + strTime
        startTime = dateEvent + "T" + strTime + "Z"
        startTime = date_to_string(parse(startTime))
        incident = self.CreateIncident(
                sport, eventGroup, home, away, startTime)

        incident = self.Call(event, incident)
        return incident

    def CreateIncident(self, sport, eventGroup, home, away, startTime):
        incident = dict()
        # incident["call"] = INCIDENT_CALLS[0]

        incident["id"] = dict()
        incident["id"]["sport"] = sport
        # eventGroupIdentifier = self.bookiesports[sport][
        # "eventgroups"][eventGroup]["identifier"]
        # incident["id"]["event_group_name"] = eventGroupIdentifier
        incident["id"]["event_group_name"] = eventGroup
        # incident["id"]["event_group_name"] = self._eventGroup
        # startTime = date_to_string(startTime)
        incident["id"]["start_time"] = startTime
        incident["arguments"] = {"whistle_start_time": startTime}
        incident["id"]["home"] = home
        incident["id"]["away"] = away
        incident["timestamp"] = date_to_string(datetime.now(tz=timezone.utc))
        incident["arguments"]["season"] = ""
        return incident

    def ForLeague(self, leagueId):
        events = self.Schedule15(leagueId)
        self.Push2Bos(events)
        events = self.Past15(leagueId)
        self.Push2Bos(events)

    def Push2Bos(self, events):
        if isinstance(events, type(None)):
            return
        for k in range(len(events)):
            while True:
                proposalsOpen = rpc.get_proposed_transactions("1.2.1")
                print("Len proposalsOpen: ", len(proposalsOpen))
                if len(proposalsOpen) <= self.maxOpenProposals:
                    break
                else:
                    time.sleep(60)
            event = events[k]
            toCp = self.ToCp(event)
            try:
                self.cp.Push2bosAll(toCp)
            except Exception as e:
                # self.failedEvents.append(toCp)
                self.failedEvents.append(event)
                print("Failed Event: ", k, toCp)
                print(e)
        return

    def PushLeague(self, leagueid, call="create"):
        if call == "create":
            events = self.Schedule15(leagueid)
        elif call == "result":
            events = self.Past15(leagueid)
        else:
            print("Wrong call")
            return
        for k in range(len(events)):
            event = events[k]
            toCp = self.ToCp(event)
            # print(k, "/", len(events), "-------event------:   ", toCp)
            print(k, "/", len(events))
            try:
                self.cp.Push2bosAll(toCp)
            except Exception as e:
                print(e)
                print("FAILED: ", event)

    def PushAll(self):
        for leagueId in leagueIds:
            self.ForLeague(leagueId)
            # self.PushLeague(leagueId)

    def WhileForThread(self):
        while self.flagWhileForThread == "run":
            print('WhileForThreadStarted')
            self.PushAll()
            print('WhileForThreadOver')
            time.sleep(self.constCheckPeriod)
        print("WhileForThred EXITED")

    def Timed(self):
        self.flagWhileForThread = "run"
        _thread.start_new_thread(self.WhileForThread, ())


class Updater:

    def __init__(self):
        self.cp = Cp()
        self.delayMax = 3600
        self.delay = 60
        self.flagWhileForThread = "stop"
        pass

    def Update(self):
        eventsAllSorted = self.cp.EventsAllSorted()
        self.eventsAllSorted = eventsAllSorted
        for k in range(len(eventsAllSorted)):
            event = eventsAllSorted.iloc[k]
            self.event = event
            print(k, "/", len(eventsAllSorted), event["start_time"])
            startTime = event["start_time"] + "Z"
            startTime = string_to_date(startTime)
            nowInUtc = datetime.now(startTime.tzinfo)
            if startTime <= nowInUtc:
                if event["status"] == "upcoming":
                    self.cp.UpdateForApi(
                        event, "in_progress")
            else:
                time2nextEvent = startTime - nowInUtc
                time2nextEvent = time2nextEvent.total_seconds()
                print("Wait Started at:", nowInUtc)
                if time2nextEvent > self.delayMax:
                    time.sleep(self.delayMax)
                else:
                    time.sleep(time2nextEvent)
                break

    def WhileForUpdate(self):
        while self.flagWhileForThread == "run":
            self.Update()
        print("WhileForUpdateThred EXITED")

    def UpdateInThread(self):
        self.flagWhileForThread = "run"
        _thread.start_new_thread(self.WhileForUpdate, ())


class FeedDetails:

    def __init__(self):
        pass

    def Leagues(self):
        leagues = requests.get(apiBase + apiAllLeagues)
        leagues = leagues.text
        leagues = json.loads(leagues)
        leagues = leagues["leagues"]
        return leagues

    def FindLeague(self):
        leagues = self.Leagues()
        while True:
            query = input("Enter Search String For Leagues: ")
            for k in range(len(leagues)):
                # print(k, "/", len(leagues))
                if query in str(leagues[k]):
                    print(leagues[k])

    def TeamsFromLeagueId(self, leagueid):
        url = apiBase + apiTeamsFromLeagueId + str(leagueid)
        teams = requests.get(url)
        teams = teams.text
        teams = json.loads(teams)
        teams = teams["teams"]
        # teamsShort = []
        for k in range(len(teams)):
            team = teams[k]
            print(
                team[
                    "strTeam"], "|", team[
                        "strTeamShort"], "|", team["strAlternate"])
            # teamShort = dict()
            # teamShort["str"]
            # team["strTeam"] =
        return teams

    def TeamsToDict(self, teams):
        participants = []
        for i in teams:
            participant = dict()
            strTeam = i["strTeam"]
            strAlternate = i["strAlternate"]
            strTeamShort = i["strTeamShort"]
            if isinstance(strAlternate, type(None)):
                strAlternate = strTeam
            elif len(strAlternate) == 0:
                strAlternate = strTeam
            if isinstance(strTeamShort, type(None)):
                strTeamShort = strTeam
            elif len(strTeamShort) == 0:
                strTeamShort = strTeam
            participant["identifier"] = strTeam
            participant["aliases"] = []
            participant["aliases"].append(strTeam)
            strAlternates = strAlternate.split(", ")
            for item in strAlternates:
                participant["aliases"].append(item)
            # participant["aliases"].append(strAlternate)
            participant["aliases"].append(strTeamShort)
            participant["name"] = dict()
            participant["name"]["en"] = strTeam
            participant["name"]["sen"] = strTeamShort
            participants.append(participant)
        return participants

    def TeamsToYaml(self, leagueId, filename):
        teams = self.TeamsFromLeagueId(leagueId)
        participants = self.TeamsToDict(teams)
        toFile = dict()
        toFile["participants"] = participants
        with open(filename, "w") as f:
            f.write(yaml.dump(toFile))
        return toFile


if __name__ == "__main__":
    feed = Feed()
    self = feed
    feedDetails = FeedDetails()
    updater = Updater()
    # leagues = feedDetails.Leagues()
    # leagues = leagues["leagues"]
    # print(leagues)

    # self = feed
    string_to_date()
