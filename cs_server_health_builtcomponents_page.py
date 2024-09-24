import pandas as pd
import psycopg2
import os
import datetime
from sqlalchemy import create_engine
from datetime import timedelta
from dotenv import load_dotenv, dotenv_values


#import dotenv values
load_dotenv()
db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_port_id = os.getenv("db_port_id")
db_hostname = os.getenv("db_hostname")
db_user = os.getenv("db_user")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

#create engine to retrieve data from local db
engine_local = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

#function to retrieve last ping status for provided ip address
def display_last_ping_response(ip_address):

    sql_retrieve_last_ping_status = (f"SELECT timestamp_log, ping_pass_fail FROM check_ping_response WHERE server_ip_address = '{ip_address}' ORDER BY timestamp_log DESC LIMIT 1")

    last_ping_response_df = pd.read_sql(sql=sql_retrieve_last_ping_status, con=engine_local)

    if last_ping_response_df.empty:

        return ([400])

    elif not last_ping_response_df.empty:

        timestamp_log = last_ping_response_df.iloc[0]['timestamp_log']
        ping_pass_fail = last_ping_response_df.iloc[0]['ping_pass_fail']

        return (200, timestamp_log, ping_pass_fail)

#function to retrieve server identities (name +  IPv4 CIDR address)
def retrieve_server_identities():

    sql_retrieve_server_identities = "SELECT * FROM server_identities"

    server_identities_df = pd.read_sql(sql=sql_retrieve_server_identities, con=engine_local)

    if server_identities_df.empty:

        return([400])
    
    elif not server_identities_df.empty:

        return(200, server_identities_df.shape[0], server_identities_df)

#function to retrieve systemload details of remote server
def retrieve_server_systemload(remote_hostname, remote_username, remote_password, remote_database, remote_port):

    try:

        #create engine based on function call arguments
        engine_remote = create_engine(f"{db_method_db}+{db_method_conn}://{remote_username}:{remote_password}@{remote_hostname}:{remote_port}/{remote_database}")

        current_date = datetime.datetime.now()
        prior_date = datetime.datetime.now() + timedelta(days=-1)

        sql_retrieve_server_systemload = (f"SELECT * FROM check_system_load WHERE timestamp_log <= '{current_date}' AND timestamp_log >= '{prior_date}' ORDER BY timestamp_log DESC")

        server_system_load_df = pd.read_sql(sql=sql_retrieve_server_systemload, con=engine_remote)

        if server_system_load_df.empty:

            return([400])
        
        elif not server_system_load_df.empty:

            #if DataFrame not empty, return average and max system load stats
            return(200, server_system_load_df.shape[0],
                server_system_load_df['cpu_temperature'].max(), round(server_system_load_df['cpu_temperature'].mean(), 1),
                server_system_load_df['memory_total'].max(), int(server_system_load_df['memory_total'].mean()),
                server_system_load_df['memory_available'].max(), int(server_system_load_df['memory_available'].mean()),
                server_system_load_df['memory_free'].max(), int(server_system_load_df['memory_free'].mean()))
        
    except:

        return([404])

#retrieve credentials of remote servers for retrieving system load stats, cronjobs and running services
def retrieve_remote_server_credentials(ip_address, database):

    try:

        sql_retrieve_remote_server_credentials = (f"SELECT * FROM server_database_credentials WHERE server_ip_address = '{ip_address}' AND server_database = '{database}'")

        retrieve_remote_server_credentials_df = pd.read_sql(sql=sql_retrieve_remote_server_credentials, con=engine_local)

        if retrieve_remote_server_credentials_df.empty:

            return([400])

        elif not retrieve_remote_server_credentials_df.empty:

            return(200,
                retrieve_remote_server_credentials_df.iloc[0]['server_ip_address_text'],
                retrieve_remote_server_credentials_df.iloc[0]['server_username'],
                retrieve_remote_server_credentials_df.iloc[0]['server_password'],
                retrieve_remote_server_credentials_df.iloc[0]['server_port'])
        
    except:

        return([404])
    
#retreive list of processes that should be running at all times on remote server
def retrieve_remote_server_list_continuous_processes(remote_hostname, remote_username, remote_password, remote_database, remote_port):

    try:

        sql_retrieve_remote_server_list_continuous_processes = (f"SELECT process_name FROM list_localhost_ongoing_processes")

        #create engine based on function call arguments
        engine_remote = create_engine(f"{db_method_db}+{db_method_conn}://{remote_username}:{remote_password}@{remote_hostname}:{remote_port}/{remote_database}")

        remote_server_listed_processes_df = pd.read_sql(sql=sql_retrieve_remote_server_list_continuous_processes, con=engine_remote)

        if remote_server_listed_processes_df.empty:

            return([400])

        elif not remote_server_listed_processes_df.empty:

            return(200, remote_server_listed_processes_df.shape[0], remote_server_listed_processes_df['process_name'].tolist())
        
    except:

        return([404])
    
#retrieve status report of continuous process
def retrieve_remote_server_status_continuous_process(remote_hostname, remote_username, remote_password, remote_database, remote_port, process_name):

    try:

        current_date = datetime.datetime.now()
        prior_date = datetime.datetime.now() + timedelta(days=-1)

        sql_retrieve_remote_server_status_continuous_process = (f"SELECT timestamp_log, process_pass_fail FROM check_ongoing_processes WHERE process_name = '{process_name}' AND timestamp_log <= '{current_date}' AND timestamp_log >= '{prior_date}' ORDER BY timestamp_log DESC")

        #create engine based on function call arguments
        engine_remote = create_engine(f"{db_method_db}+{db_method_conn}://{remote_username}:{remote_password}@{remote_hostname}:{remote_port}/{remote_database}")

        remote_server_listed_continuous_process_status_df = pd.read_sql(sql=sql_retrieve_remote_server_status_continuous_process, con=engine_remote)

        if remote_server_listed_continuous_process_status_df.empty:

            return([400])

        elif not remote_server_listed_continuous_process_status_df.empty:

            number_of_entries = remote_server_listed_continuous_process_status_df.shape[0]
            number_of_fails = len(remote_server_listed_continuous_process_status_df[remote_server_listed_continuous_process_status_df['process_pass_fail'] == 'Fail'])
            last_entry_timestamp_log = remote_server_listed_continuous_process_status_df.iloc[0]['timestamp_log']

            return(200, number_of_entries, number_of_fails, last_entry_timestamp_log)

    except:

        return([404])
    
#retrieve list of tables that have a scheduled (re)load of data
def retrieve_remote_server_scheduled_reloads(remote_hostname, remote_username, remote_password, remote_database, remote_port):

    try:

        sql_retrieve_remote_server_scheduled_reloads = (f"SELECT database_name, table_name, load_frequency_hours FROM database_table_load_frequency")

        #create engine based on function call arguments
        engine_remote = create_engine(f"{db_method_db}+{db_method_conn}://{remote_username}:{remote_password}@{remote_hostname}:{remote_port}/{remote_database}")

        retrieve_remote_server_scheduled_reloads_df = pd.read_sql(sql=sql_retrieve_remote_server_scheduled_reloads, con=engine_remote)

        if retrieve_remote_server_scheduled_reloads_df.empty:

            return([400])
        
        elif not retrieve_remote_server_scheduled_reloads_df.empty:

            return(200, retrieve_remote_server_scheduled_reloads_df.shape[0], retrieve_remote_server_scheduled_reloads_df)

    except:

        return([404])

#retrieve if last scheduled API call/data load has entries in tables
def retrieve_remote_server_scheduled_reload_status(remote_hostname, remote_username, remote_password, remote_database, remote_port, remote_table, remote_reload_frequency):

    try:

        current_date = datetime.datetime.now()
        frequency_hours = int(remote_reload_frequency)
        prior_date = current_date + timedelta(hours=-frequency_hours)

        #create engine based on function call arguments
        engine_remote = create_engine(f"{db_method_db}+{db_method_conn}://{remote_username}:{remote_password}@{remote_hostname}:{remote_port}/{remote_database}")

        sql_retrieve_remote_server_scheduled_reload_status = (f"SELECT id, datesync_datetime FROM {remote_table} WHERE datesync_datetime <= '{current_date}' AND datesync_datetime >= '{prior_date}' ORDER BY datesync_datetime DESC")

        retrieve_remote_server_scheduled_reload_status_df = pd.read_sql(sql=sql_retrieve_remote_server_scheduled_reload_status, con=engine_remote)

        if retrieve_remote_server_scheduled_reload_status_df.empty:

            return([400])
        
        elif not retrieve_remote_server_scheduled_reload_status_df.empty:

            return(200, retrieve_remote_server_scheduled_reload_status_df.shape[0], retrieve_remote_server_scheduled_reload_status_df.iloc[0]['datesync_datetime'])

    except:

        return([404])