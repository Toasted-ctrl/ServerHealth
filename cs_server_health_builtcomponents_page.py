import pandas as pd
import psycopg2
import os

from sqlalchemy import create_engine
from dotenv import load_dotenv, dotenv_values

load_dotenv()
db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_port_id = os.getenv("db_port_id")
db_hostname = os.getenv("db_hostname")
db_user = os.getenv("db_user")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

def display_last_ping_response(ip_address):

    sql_retrieve_last_ping_status = (f"SELECT timestamp_log, ping_pass_fail FROM check_ping_response WHERE server_ip_address = '{ip_address}' ORDER BY timestamp_log DESC LIMIT 1")

    last_ping_response_df = pd.read_sql(sql=sql_retrieve_last_ping_status, con=engine)

    if last_ping_response_df.empty:

        timestamp_log = "Error: Unable to retrieve."
        ping_pass_fail = "Error: Unable to retrieve."

    elif not last_ping_response_df.empty:

        timestamp_log = last_ping_response_df.iloc[0]['timestamp_log']
        ping_pass_fail = last_ping_response_df.iloc[0]['ping_pass_fail']

    return (timestamp_log, ping_pass_fail)

def retrieve_server_identities():

    sql_retrieve_server_identities = "SELECT * FROM server_identities"

    server_identities_df = pd.read_sql(sql=sql_retrieve_server_identities, con=engine)

    if server_identities_df.empty:

        return([400])
    
    elif not server_identities_df.empty:

        return(200, server_identities_df.shape[0], server_identities_df)