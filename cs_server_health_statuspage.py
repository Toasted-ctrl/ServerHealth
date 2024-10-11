#!/usr/bin/env python3

import streamlit as st
import os
import requests
import datetime
from dotenv import load_dotenv

#load api key and main api link
load_dotenv()
api_key = os.getenv("api_key")
api_link = os.getenv("api_link")

#link extensions for separate api calls
extension_remote_server_identities = "/remote_server_identities"
extension_remote_server_last_ping_response = "/remote_server_last_ping_response"
extension_remote_server_systemload = "/remote_server_systemload"
extension_remote_server_running_services = "/remote_server_running_processes"
extension_remote_server_running_services_status = "/remote_server_running_process_status"
extension_remote_server_scheduled_reloads = "/remote_server_scheduled_reloads"
extension_remote_server_scheduled_reloads_status = "/remote_server_scheduled_reload_status"

#error keys to check for in JSON objects
check_error_key = "error"

st.set_page_config(page_title="Server status")

st.title("Server overview")

date_of_retrieving_server_identities = datetime.datetime.now()
st.text(f"Date: {date_of_retrieving_server_identities}")

def create_list_active_servers():

    request_remote_server_identities_url = (f"{api_link}{extension_remote_server_identities}")
    request_remote_server_identities_params = {'api_key' : api_key}

    request_remote_server_identities_response = requests.get(request_remote_server_identities_url, params=request_remote_server_identities_params)

    if request_remote_server_identities_response.status_code == 404:

        st.text("error on calling api")

    elif request_remote_server_identities_response.status_code == 200:

        if check_error_key in request_remote_server_identities_response.json():

            st.text(f"error code: {request_remote_server_identities_response.json()['error']}")

        elif not check_error_key in request_remote_server_identities_response.json():

            number_of_remote_servers = len(request_remote_server_identities_response.json())

            #create list of remote servers listed in control database
            for i in range (number_of_remote_servers):

                remote_server_name = request_remote_server_identities_response.json()[i]['server_name']
                remote_server_ip_address = request_remote_server_identities_response.json()[i]['server_ip_address'].replace("/32", "")

                st.text(f"Server {i}: {remote_server_name} / {remote_server_ip_address}")
 
            #for each server, create report
            for i in range (number_of_remote_servers):

                st.divider()

                remote_server_name = request_remote_server_identities_response.json()[i]['server_name']
                remote_server_ip_address = request_remote_server_identities_response.json()[i]['server_ip_address'].replace("/32", "")

                st.header(f"Server {i}: {remote_server_name}")
                st.text(f"Server IP address: {remote_server_ip_address}")

                #server last ping section

                request_remote_server_last_ping_url = (f"{api_link}{extension_remote_server_last_ping_response}")
                request_remote_server_last_ping_params = {'api_key': api_key, 'hostname': remote_server_ip_address}

                request_remote_server_last_ping_response = requests.get(request_remote_server_last_ping_url, params=request_remote_server_last_ping_params)

                st.text(f"Server's last ping response:")

                if request_remote_server_last_ping_response.status_code == 404:

                    st.text(f"Error: API call error")

                elif request_remote_server_last_ping_response.status_code == 200:

                    st.text(f"""
                          >> Ping timestamp: {request_remote_server_last_ping_response.json()['ping_timestamp_log']}
                          >> Ping status: {request_remote_server_last_ping_response.json()['ping_status']}
                          """)
                
                #server systemload section

                st.subheader(f"Server systemload during last 24 hours")

                request_remote_server_systemload_url = (f"{api_link}{extension_remote_server_systemload}")
                request_remote_server_systemload_params = {'api_key': api_key, 'hostname': remote_server_ip_address}

                request_remote_server_systemload_response = requests.get(request_remote_server_systemload_url, params=request_remote_server_systemload_params)

                if request_remote_server_systemload_response.status_code == 404:

                    st.text(f"Error: API call error")

                elif request_remote_server_systemload_response.status_code == 200:

                    if check_error_key in request_remote_server_systemload_response.json():

                        st.text(f"Error: {request_remote_server_systemload_response.json()['error']}")

                    elif not check_error_key in request_remote_server_systemload_response.json():

                        st.text(f"Number of entries: {request_remote_server_systemload_response.json()['systemload_records']}")
                        st.text(f"Avg CPU temperature: {request_remote_server_systemload_response.json()['systemload_cup_temp_mean']} (Max: {request_remote_server_systemload_response.json()['systemload_cpu_temp_max']})")
                        st.text(f"System memory:")
                        st.text(f"""
                              >> Total - {request_remote_server_systemload_response.json()['systemload_memory_total']}
                              >> Available - Avg: {request_remote_server_systemload_response.json()['systemload_memory_available_mean']}, Max: {request_remote_server_systemload_response.json()['systemload_memory_available_max']}
                              >> Free - Avg: {request_remote_server_systemload_response.json()['systemload_memory_free_mean']}, Max: {request_remote_server_systemload_response.json()['systemload_memory_free_max']}
                              """)
                        
                # running services section

                st.subheader(f"Running services")

                request_remote_server_running_services_url = (f"{api_link}{extension_remote_server_running_services}")
                request_remote_server_running_services_params = {'api_key': api_key, 'hostname': remote_server_ip_address}

                request_remote_server_running_services_response = requests.get(request_remote_server_running_services_url, params=request_remote_server_running_services_params)

                if request_remote_server_running_services_response.status_code == 404:

                    st.text(f"Error: API call error")

                elif request_remote_server_running_services_response.status_code == 200:

                    if check_error_key in request_remote_server_running_services_response.json():

                        st.text(f"Error: {request_remote_server_running_services_response.json()['error']}")

                    elif not check_error_key in request_remote_server_running_services_response.json():

                        number_of_running_services = len(request_remote_server_running_services_response.json())

                        for i in range (number_of_running_services):

                            running_service_name = request_remote_server_running_services_response.json()[i]['process_name']

                            st.text(f"Process name: {running_service_name}")

                            #running services status section

                            request_remote_server_running_services_status_url = (f"{api_link}{extension_remote_server_running_services_status}")
                            request_remote_server_running_services_status_params = {'api_key': api_key, 'hostname': remote_server_ip_address, 'process_name': running_service_name}

                            request_remote_server_running_services_status_response = requests.get(request_remote_server_running_services_status_url, params=request_remote_server_running_services_status_params)

                            if request_remote_server_running_services_status_response.status_code == 404:

                                st.text(f"Error: API call error")

                            elif request_remote_server_running_services_status_response.status_code == 200:

                                if check_error_key in request_remote_server_running_services_status_response.json():

                                    st.text(f"Error: {request_remote_server_running_services_status_response.json()['error']}")

                                elif not check_error_key in request_remote_server_running_services_status_response.json():

                                    st.text(f"""
                                          >> Last reload status: {request_remote_server_running_services_status_response.json()['last_measurement']}
                                          >> 24h checks: {request_remote_server_running_services_status_response.json()['24h_measurements']}
                                          >> 24h fails: {request_remote_server_running_services_status_response.json()['24h_fails']}
                                          """)
                                    
                # API call/data loads section

                st.subheader(f"API calls/data loads")

                request_remote_server_data_reloads_url = (f"{api_link}{extension_remote_server_scheduled_reloads}")
                request_remote_server_data_reloads_params = {'api_key': api_key, 'hostname': remote_server_ip_address}

                request_remote_server_data_reloads_response = requests.get(request_remote_server_data_reloads_url, params=request_remote_server_data_reloads_params)

                if request_remote_server_data_reloads_response.status_code == 404:

                    st.text(f"Error: API call error")

                elif request_remote_server_data_reloads_response.status_code == 200:

                    if check_error_key in request_remote_server_data_reloads_response.json():

                        st.text(f"Error: {request_remote_server_data_reloads_response.json()['error']}")

                    elif not check_error_key in request_remote_server_data_reloads_response.json():

                        number_of_data_reloads = len(request_remote_server_data_reloads_response.json())

                        # section for each individual api call / data load

                        for i in range (number_of_data_reloads):

                            reload_database_name = request_remote_server_data_reloads_response.json()[i]['database_name']
                            reload_table_name = request_remote_server_data_reloads_response.json()[i]['table_name']
                            reload_load_frequency_hours = request_remote_server_data_reloads_response.json()[i]['load_frequency_hours']

                            st.text(f"DB name: {reload_database_name}, Table name: {reload_table_name}")

                            request_remote_server_data_reloads_status_url = (f"{api_link}{extension_remote_server_scheduled_reloads_status}")
                            request_remote_server_data_reloads_status_params = {'api_key': api_key, 'hostname': remote_server_ip_address, 'remote_database_name': reload_database_name, 'reload_name': reload_table_name, 'reload_frequency': reload_load_frequency_hours}

                            request_remote_server_data_reloads_status_response = requests.get(request_remote_server_data_reloads_status_url, params=request_remote_server_data_reloads_status_params)

                            if request_remote_server_data_reloads_status_response.status_code == 404:

                                st.text(f"Error: API call error")

                            elif request_remote_server_data_reloads_status_response.status_code == 200:

                                if check_error_key in request_remote_server_data_reloads_status_response.json():

                                    if request_remote_server_data_reloads_status_response.json()['error'] == "empty_dataframe_scheduled_reloads":

                                        st.text(f"""
                                                >> Last reload status: FAILED
                                                >> Reloads every {reload_load_frequency_hours}.
                                                """)
                                        
                                    else:

                                        st.text(f"Error: {request_remote_server_data_reloads_status_response.json()['error']}")

                                elif not check_error_key in request_remote_server_data_reloads_status_response.json():

                                    st.text(f"""
                                    >> Last reload status: COMPLETED
                                    >> Reloads every {reload_load_frequency_hours}. Last reload: {request_remote_server_data_reloads_status_response.json()['last_reload_timestamp']}
                                    >> Number of entries: {request_remote_server_data_reloads_status_response.json()['rows_added']}
                                    """)

create_list_active_servers()