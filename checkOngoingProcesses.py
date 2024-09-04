import os
import subprocess
from dotenv import dotenv_values, load_dotenv


load_dotenv()
ongoing_process_server_1 = os.getenv("server_1_ongoing_process_001")

def checkOngoingProcesses(processName):

    process_check_command = ["ps aux | grep [m]ain.py | grep -v grep"]

    print(subprocess.check_output(process_check_command))

checkOngoingProcesses(ongoing_process_server_1)