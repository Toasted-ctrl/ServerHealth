import os
import platform
import subprocess
import datetime
from dotenv import dotenv_values, load_dotenv

#determine platform
local_platform = platform.system()

#load dotenv objects (server hostnames)
load_dotenv()
server_1_hostname = os.getenv("server_1_hostname")
server_2_hostname = os.getenv("server_2_hostname")

#ping function
def ping_server(server_hostname):

    #create datetime timestamp for inclusion into ping report
    ping_timestamp = datetime.datetime.now()
    print(ping_timestamp)

    #determine parameter for ping based on OS. Windows OS = -n, UNIX = -c
    if local_platform.lower() == "windows":

        subprocess_parameter = "-n"

    else:

        print("UNIX machine")

        subprocess_parameter = "-c"

    #command line ping Windows: ping -n 1 <hostname>
    #command line ping UNIX: ping -c 1 <hostname>

    #create ping command based on operating system
    ping_command = ["ping", subprocess_parameter, "1", server_hostname]

    #execute ping command
    ping_response = subprocess.call(ping_command)

    #return ping response as boolean. 0 (True) indicates successful ping, 1 (False) indicates unsucessful ping
    return ping_response == 0

result = ping_server(server_1_hostname)
print(result)