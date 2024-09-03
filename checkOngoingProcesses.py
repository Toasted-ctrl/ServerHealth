import os
import subprocess
from dotenv import dotenv_values, load_dotenv


load_dotenv()
ongoing_process_server_1 = os.getenv("server_1_ongoing_process_001")

def process_status(process_name):

    check_process_command = ["pgrep", "-af", process_name]

    try:

        output = subprocess.check_output(check_process_command)

        if output == 0:

            print(f"{check_process_command} is running")

    except subprocess.CalledProcessError as e:

        print(e)

process_status(ongoing_process_server_1)