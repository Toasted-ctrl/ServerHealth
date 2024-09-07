

from serverHealth_builtComponents import listProcessesToBeChecked, checkOngoingProcesses


retrieveprocesses = listProcessesToBeChecked()

if retrieveprocesses[0] == 200:

    listProcesses = retrieveprocesses[1]

    for listProcess in listProcesses:

        processOngoing = checkOngoingProcesses(listProcess)

        if processOngoing == 200:

            print(f"{listProcess} is currently running")

        elif processOngoing == 400:

            print(f"{listProcess} is not running.")

else:
        
    print(retrieveprocesses[0])