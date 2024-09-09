#!/usr/bin/env python3

from serverHealth_builtComponents import listProcessesToBeChecked, checkOngoingProcesses, insertCheckOngoingProcessToDB

try:

    retrieveprocesses = listProcessesToBeChecked()

    if retrieveprocesses[0] == 200:

        listProcesses = retrieveprocesses[1]

        for listProcess in listProcesses:

            processOngoing = checkOngoingProcesses(listProcess)

            if processOngoing == 200:

                processPassFail = "Pass"

            elif processOngoing == 400:

                processPassFail = "Fail"

            insertCheckOngoingProcessToDB(listProcess, processPassFail)

except Exception as e:

    print(e)