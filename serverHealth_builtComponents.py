import os
import subprocess
import pandas as pd
from sqlalchemy import create_engine
from dotenv import dotenv_values, load_dotenv

load_dotenv()

db_database = os.getenv("db_database")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_hostname = os.getenv("db_hostname")
db_port_id = os.getenv("db_port_id")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

def listProcessesToBeChecked():

    retrieveProcesses_sql = str(f"SELECT process_name FROM list_localhost_ongoing_processes")

    df_listProcesses = pd.read_sql(sql=retrieveProcesses_sql, con=engine)

    listProcesses = df_listProcesses['process_name'].to_list()

    if not df_listProcesses.empty:

        return (200, listProcesses)
    
    elif df_listProcesses.empty:

        return ([400])
    
    else:

        return ([404])
    

def checkOngoingProcesses(processName):

    process_check_command = [f"""ps aux | grep {processName} | grep -v grep"""]

    try:
        
        subprocess.check_output(process_check_command, shell=True)

        return(200)

    except subprocess.CalledProcessError as e:

        return(400)