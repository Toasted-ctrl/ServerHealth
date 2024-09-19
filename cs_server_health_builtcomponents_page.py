import pandas as pd
import psycopg2
import os
import datetime
from sqlalchemy import create_engine
from datetime import timedelta
from dotenv import load_dotenv, dotenv_values

load_dotenv()
db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_port_id = os.getenv("db_port_id")
db_hostname = os.getenv("db_hostname")
db_user = os.getenv("db_user")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

engine_local = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

def display_last_ping_response(ip_address):

    sql_retrieve_last_ping_status = (f"SELECT timestamp_log, ping_pass_fail FROM check_ping_response WHERE server_ip_address = '{ip_address}' ORDER BY timestamp_log DESC LIMIT 1")

    last_ping_response_df = pd.read_sql(sql=sql_retrieve_last_ping_status, con=engine_local)

    if last_ping_response_df.empty:

        timestamp_log = "Error: Unable to retrieve."
        ping_pass_fail = "Error: Unable to retrieve."

    elif not last_ping_response_df.empty:

        timestamp_log = last_ping_response_df.iloc[0]['timestamp_log']
        ping_pass_fail = last_ping_response_df.iloc[0]['ping_pass_fail']

    return (timestamp_log, ping_pass_fail)

def retrieve_server_identities():

    sql_retrieve_server_identities = "SELECT * FROM server_identities"

    server_identities_df = pd.read_sql(sql=sql_retrieve_server_identities, con=engine_local)

    if server_identities_df.empty:

        return([400])
    
    elif not server_identities_df.empty:

        return(200, server_identities_df.shape[0], server_identities_df)
    
def retrieve_server_systemload(remote_hostname, remote_username, remote_password, remote_database, remote_port):

    try:

        engine_remote = create_engine(f"{db_method_db}+{db_method_conn}://{remote_username}:{remote_password}@{remote_hostname}:{remote_port}/{remote_database}")

        current_date = datetime.datetime.now()
        prior_date = datetime.datetime.now() + timedelta(days=-1)

        sql_retrieve_server_systemload = (f"SELECT * FROM check_system_load WHERE timestamp_log <= '{current_date}' AND timestamp_log >= '{prior_date}' ORDER BY timestamp_log DESC")

        server_system_load_df = pd.read_sql(sql=sql_retrieve_server_systemload, con=engine_remote)

        if server_system_load_df.empty:

            return([400])
        
        elif not server_system_load_df.empty:

            return(200, server_system_load_df.shape[0],
                server_system_load_df['cpu_temperature'].max(), round(server_system_load_df['cpu_temperature'].mean(), 1),
                server_system_load_df['memory_total'].max(), int(server_system_load_df['memory_total'].mean()),
                server_system_load_df['memory_available'].max(), int(server_system_load_df['memory_available'].mean()),
                server_system_load_df['memory_free'].max(), int(server_system_load_df['memory_free'].mean()))
        
    except:

        return([404])