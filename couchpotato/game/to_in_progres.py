from cp_local import cp_local
import pandas as pd
import datetime as dt
import time

cp = cp_local.Cp()

while True:

    eventsAllSorted = cp.EventsAllSortedForApi()

    eventsAllSorted = pd.DataFrame(eventsAllSorted)

    for k in range(len(eventsAllSorted)):
        event = eventsAllSorted.iloc[k]
        print(k, "/", len(eventsAllSorted), event["start_time"])
        startTime = event["start_time"] + "Z"
        startTime = cp_local.string_to_date(startTime)
        nowInUtc = dt.datetime.now(startTime.tzinfo)
        if startTime < nowInUtc:
            if event["status"] == "upcoming":
                cp.UpdateForApiWithPotato(event, "in_progress", "cpai")
                # print("moved to in_prgress:", event)
            pass
        else:
            break
    time.sleep(60)
