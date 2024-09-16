import os
import platform
import subprocess
import datetime
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import dotenv_values, load_dotenv

load_dotenv()
db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_port_id = os.getenv("db_port_id")
db_hostname = os.getenv("db_hostname")
db_user = os.getenv("db_user")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

#ping function
def ping_server(server_hostname):

    local_platform = platform.system()

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

def retrieve_host_machines_ip_addresses():

    sql_retrieve_ip_address = "SELECT server_ip_address FROM server_identities"

    ip_address_df = pd.read_sql(sql=sql_retrieve_ip_address, con=engine)

    if ip_address_df.empty:

        return([400])
    
    elif not ip_address_df.empty:

        ip_address_list = ip_address_df['server_ip_address'].to_list()

        return(200, ip_address_list)
    
def store_ping_response(ip_address, ping_response):

    conn = None
    cursor = None

    try:
        
        conn = psycopg2.connect(
            database = db_database,
            user = db_user,
            password = db_password,
            host = db_hostname,
            port = db_port_id)
        
        cursor = conn.cursor()

        insert_query = (f"INSERT INTO check_ping_response (server_ip_address, ping_pass_fail) VALUES ('{ip_address}', '{ping_response}')")
        
        cursor.execute(insert_query)

        conn.commit()

    except Exception as e:

        print(f"Error: {e}")

    finally:

        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()