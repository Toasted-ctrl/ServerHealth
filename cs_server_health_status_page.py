import streamlit as st
import pandas as pd
import datetime
from cs_server_health_builtcomponents_page import display_last_ping_response, retrieve_server_identities, retrieve_remote_server_credentials, retrieve_server_systemload, retrieve_remote_server_list_continuous_processes, retrieve_remote_server_status_continuous_process, retrieve_remote_server_scheduled_reloads, retrieve_remote_server_scheduled_reload_status

#page title
st.set_page_config(page_title="This is my first page")

st.title("Server overview")

@st.cache_data(ttl=60)
def create_list_active_servers():

    server_identity_dataframe = retrieve_server_identities()

    date_of_retrieving_server_identities = datetime.datetime.now()
    st.text(f"Date: {date_of_retrieving_server_identities}")

    if server_identity_dataframe[0] == 400:

        st.text(f"Currently no servers in checking database.")

    if server_identity_dataframe[0] == 200:

        server_dataframe = server_identity_dataframe[2]

        st.dataframe(server_dataframe)
        number_of_servers = server_identity_dataframe[1]

        for i in range(number_of_servers):

            server_name = server_dataframe.iloc[i]['server_name']
            server_ip_address = server_dataframe.iloc[i]['server_ip_address']

            server_ping_check = display_last_ping_response(server_ip_address)
            server_last_ping_timestamp = server_ping_check[0]
            server_last_ping_status = server_ping_check[1]

            st.divider()
            st.header(f"Server {i}: {server_name}")

            st.text(f"Server IP address: {server_ip_address}")

            st.text(f"Last ping timestamp: {server_last_ping_timestamp}")
            st.text(f"Last ping status: {server_last_ping_status}")

            st.subheader(f"Server systemload during the last 24 hours")

            remote_server_credentials = retrieve_remote_server_credentials(server_ip_address, 'serverhealth_logs')

            if remote_server_credentials[0] == 400:

                st.text(f"Error, cannot display system load: Missing credentials.")

            elif remote_server_credentials[0] == 200:

                remote_server_ip_address = remote_server_credentials[1]
                remote_server_username = remote_server_credentials[2]
                remote_server_password = remote_server_credentials[3]
                remote_server_port = remote_server_credentials[4]

                remote_server_system_load = retrieve_server_systemload(remote_server_ip_address, remote_server_username, remote_server_password, 'serverhealth_logs', remote_server_port)

                if remote_server_system_load[0] == 400:

                    st.text(f"Error, cannot display system load: Missing system logs.")

                elif remote_server_system_load[0] == 404:

                    st.text(f"Unexpected error, cannot display system load.")

                elif remote_server_system_load[0] == 200:

                    st.text(f"Number of entries: {remote_server_system_load[1]}")
                    st.text(f"Average CPU temperature: {remote_server_system_load[3]} (Max: {remote_server_system_load[2]})")
                    st.text(f"System memory:")
                    st.text(f"""
                            >> Total - {remote_server_system_load[5]}
                            >> Available - Avg: {remote_server_system_load[7]}, Max: {remote_server_system_load[6]}
                            >> Free - Avg: {remote_server_system_load[9]}, Max: {remote_server_system_load[8]}
                            """)

                st.subheader(f"Running services")

                remote_server_listed_continuous_processes = retrieve_remote_server_list_continuous_processes(remote_server_ip_address, remote_server_username, remote_server_password, 'serverhealth_logs', remote_server_port)

                if remote_server_listed_continuous_processes[0] == 400:

                    st.text(f"No processes listed on remote server.")

                elif remote_server_listed_continuous_processes[0] == 404:

                    st.text(f"Unexpected error, cannot display listed processes.")

                elif remote_server_listed_continuous_processes[0] == 200:

                    for i in range(remote_server_listed_continuous_processes[1]):

                        remote_server_continuous_process_name = remote_server_listed_continuous_processes[2][i]

                        st.text(f"Process name: {remote_server_continuous_process_name}")

                        remote_server_continuous_process_status = retrieve_remote_server_status_continuous_process(remote_server_ip_address, remote_server_username, remote_server_password, 'serverhealth_logs', remote_server_port, remote_server_continuous_process_name)

                        if remote_server_continuous_process_status[0] == 400:

                            st.text(f">> Error: status for '{remote_server_continuous_process_name}' could not be found.")

                        elif remote_server_continuous_process_status[0] == 404:

                            st.text(f">> Unexpected error, cannot display status for '{remote_server_continuous_process_name}'.")

                        elif remote_server_continuous_process_status[0] == 200:

                            st.text(f"""
                                    >> Last status update: {remote_server_continuous_process_status[3]}
                                    >> Entries past 24 hours: {remote_server_continuous_process_status[1]}
                                    >> Fails past 24 hours: {remote_server_continuous_process_status[2]}
                                    """)

                st.subheader(f"API calls/data loads")

                list_scheduled_data_loads = retrieve_remote_server_scheduled_reloads(remote_server_ip_address, remote_server_username, remote_server_password, 'serverhealth_logs', remote_server_port)

                if list_scheduled_data_loads[0] == 400:

                    st.text(f"No scheduled API calls/data loads listed on remote server.")

                elif list_scheduled_data_loads[0] == 404:

                    st.text(f"Unexpected error, cannot display scheduled API calls/data loads.")

                elif list_scheduled_data_loads[0] == 200:

                    for i in range(list_scheduled_data_loads[1]):

                        reload_DataFrame = list_scheduled_data_loads[2]
                        reload_database_name = reload_DataFrame.iloc[i]['database_name']
                        reload_table_name = reload_DataFrame.iloc[i]['table_name']
                        reload_frequency = reload_DataFrame.iloc[i]['load_frequency_hours']

                        reload_status = retrieve_remote_server_scheduled_reload_status(remote_server_ip_address, remote_server_username, remote_server_password, reload_database_name, remote_server_port, reload_table_name, reload_frequency)

                        st.text(f"DB Name: {reload_database_name}, Table name: {reload_table_name}")

                        if reload_status[0] == 400:

                            st.text(f"""
                                    >> Last reload status: FAILED TO RELOAD
                                    >> Reloads every {reload_frequency} hours.
                                    """)

                        elif reload_status[0] == 404:

                            st.text(f">> Unexpected error: Could not retrieve reload information.")

                        elif reload_status[0] == 200:

                            st.text(f"""
                                    >> Last reload status: COMPLETED
                                    >> Reloads every {reload_frequency} hours. Last reload: {reload_status[2]}
                                    >> Number of entries: {reload_status[1]}
                                    """)

create_list_active_servers()