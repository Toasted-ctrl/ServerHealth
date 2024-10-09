import streamlit as st
import datetime
import os
import requests
from dotenv import load_dotenv

#load api key and main api link
load_dotenv()
api_key = os.getenv("api_key")
api_link = os.getenv("api_link")

#link extensions for separate api calls
extension_remote_server_identities = "/remote_server_identities"
extension_remote_server_last_ping_response = "/remote_server_last_ping_response"

#error keys to check for in JSON objects
check_error_key = "error"

def create_list_active_servers():

    request_remote_server_identities_url = (f"{api_link}{extension_remote_server_identities}")
    request_remote_server_identities_params = {'api_key' : api_key}

    request_remote_server_identities_response = requests.get(request_remote_server_identities_url, params=request_remote_server_identities_params)

    if request_remote_server_identities_response.status_code == 404:

        print ("error on calling api")

    elif request_remote_server_identities_response.status_code == 200:

        print ("Success")

        if check_error_key in request_remote_server_identities_response.json():

            print ("error in json response")
            print (f"error code: {request_remote_server_identities_response.json()['error']}")

        elif not check_error_key in request_remote_server_identities_response.json():

            number_of_remote_servers = len(request_remote_server_identities_response.json())

            #create list of remote servers listed in control database
            for i in range (number_of_remote_servers):

                remote_server_name = request_remote_server_identities_response.json()[i]['server_name']
                remote_server_ip_address = request_remote_server_identities_response.json()[i]['server_ip_address'].replace("/32", "")

                print(f"Server {i}: {remote_server_name} / {remote_server_ip_address}")

                #TODO: INSERT STREAMLIT DIVIDER HERE

                print("Streamlit divider here")
 
            for i in range (number_of_remote_servers):

                remote_server_name = request_remote_server_identities_response.json()[i]['server_name']
                remote_server_ip_address = request_remote_server_identities_response.json()[i]['server_ip_address'].replace("/32", "")

                #for each remote server, check last ping response

                request_remote_server_last_ping_response_url = (f"{api_link}{extension_remote_server_last_ping_response}")
                request_remote_server_last_ping_response_params = {'api_key': api_key, 'hostname': remote_server_ip_address}

                request_remote_server_last_ping_response_response = requests.get(request_remote_server_last_ping_response_url, params=request_remote_server_last_ping_response_params)

                if request_remote_server_last_ping_response_response.status_code == 404:

                    print(f"Server {i}: API call error")

                elif request_remote_server_last_ping_response_response.status_code == 200:

                    print(f"Server {i}: Success on calling last ping response")
                

create_list_active_servers()