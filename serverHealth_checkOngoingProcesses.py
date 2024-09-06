import os
import subprocess
import datetime
from dotenv import dotenv_values, load_dotenv


load_dotenv()
ongoing_process_server_1 = os.getenv("server_1_ongoing_process_001")

def checkOngoingProcesses(processName):

    process_check_command = [f"""ps aux | grep {ongoing_process_server_1} | grep -v grep"""]

    try:

        process_check_call = subprocess.check_output(process_check_command, shell=True)

        print(process_check_call)

        print("Service running")

    except subprocess.CalledProcessError as e:

        print(e.output)

        print("Service not running")


checkOngoingProcesses(ongoing_process_server_1)