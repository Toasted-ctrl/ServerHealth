import streamlit as st
import pandas as pd
import datetime
import os
from cs_server_health_builtcomponents_page import display_last_ping_response, retrieve_server_identities

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

create_list_active_servers()