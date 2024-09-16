import streamlit as st
import pandas as pd
import os
from cs_server_health_builtcomponents_page import display_last_ping_response
from dotenv import dotenv_values, load_dotenv

#import server ip address
server_1 = os.getenv("control_server_host_machine_1")

#page title
st.set_page_config(page_title="This is my first page")

st.title("Server status page")



st.divider()

st.header("S1: Honey Badger")

server_1_ping_response = display_last_ping_response(server_1)

st.text(f"Last ping: {server_1_ping_response[0]}")
st.text(f"Ping response: {server_1_ping_response[1]}")


st.divider()

st.header("S2: Hippopotamus")
st.text("Placeholder for second server data.")