import streamlit as st
import pandas as pd
import datetime
from cs_server_health_builtcomponents_page import display_last_ping_response, retrieve_server_identities, retrieve_remote_server_credentials, retrieve_server_systemload

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

                    st.text(f"Error, cannot display system load: Unexpected error.")

                elif remote_server_system_load[0] == 200:

                    st.text(f"Number of entries: {remote_server_system_load[1]}")
                    st.text(f"Average CPU temperature: {remote_server_system_load[3]} (Max: {remote_server_system_load[2]})")
                    st.text(f"System memory, total: {remote_server_system_load[5]}")
                    st.text(f"System memory, available: {remote_server_system_load[7]} (Max: {remote_server_system_load[6]})")
                    st.text(f"System memory, free: {remote_server_system_load[9]} (Max: {remote_server_system_load[8]})")

            st.subheader(f"Running services")

            st.subheader(f"API calls/data loads")

create_list_active_servers()