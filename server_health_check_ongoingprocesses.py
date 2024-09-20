#!/usr/bin/env python3

from server_health_builtcomponents import listProcessesToBeChecked, checkOngoingProcesses, insertCheckOngoingProcessToDB

try:

    #retrieve processes that should be running at all times
    retrieveprocesses = listProcessesToBeChecked()

    if retrieveprocesses[0] == 200:

        #create list of processes if response to listProcessesToBeChecked is 200
        listProcesses = retrieveprocesses[1]

        #for every processes in list, try below
        for listProcess in listProcesses:

            #call checkOngoingProcesses to check if process is running
            processOngoing = checkOngoingProcesses(listProcess)

            if processOngoing == 200:

                processPassFail = "Pass"

            elif processOngoing == 400:

                processPassFail = "Fail"

            #insert result into db
            insertCheckOngoingProcessToDB(listProcess, processPassFail)

except Exception as e:

    print(e)