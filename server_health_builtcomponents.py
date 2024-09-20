import os
import subprocess
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, insert
from dotenv import dotenv_values, load_dotenv

#import dotenv values
load_dotenv()

db_database = os.getenv("db_database")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_hostname = os.getenv("db_hostname")
db_port_id = os.getenv("db_port_id")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

#create engine to connect to db
engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

#function to retrieve list of procceses that require checking
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
    
#function to check if process is currently running
def checkOngoingProcesses(processName):

    process_check_command = [f"""ps aux | grep {processName} | grep -v grep"""]

    try:
        
        subprocess.check_output(process_check_command, shell=True)

        return(200)

    except subprocess.CalledProcessError as e:

        return(400)

#function to insert process check into db
def insertCheckOngoingProcessToDB (processName, passOrFail):

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

        insert_query = (f"INSERT INTO check_ongoing_processes (process_name, process_pass_fail) VALUES ('{processName}', '{passOrFail}')")
        
        cursor.execute(insert_query)

        conn.commit()
        
    except Exception as e:
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

#function to check cpu temperature
def check_system_cpu_temperature():

    try:

        shell_command_cpu_temperature = ['vcgencmd', 'measure_temp']
        
        shell_return = subprocess.check_output(shell_command_cpu_temperature).decode('utf-8')

        cpu_temperature = float(shell_return.replace("temp=", "").replace("'C", ""))
        
        return(200, cpu_temperature)

    except subprocess.CalledProcessError:

        return([400])

#function to check total system memory
def check_system_memory_total():

    try:

        shell_command_check_memory_total = [F"""less /proc/meminfo | grep MemTotal"""]
        
        shell_return_check_memory_total = subprocess.check_output(shell_command_check_memory_total, shell=True).decode('utf-8')

        system_memory_total = int(shell_return_check_memory_total.replace("MemTotal:", "").replace(" kB", "").replace(" ", ""))

        return(200, system_memory_total)

    except subprocess.CalledProcessError:

        return([400])

#function to check total available memory
def check_system_memory_available():

    try:

        shell_command_check_memory_available = [F"""less /proc/meminfo | grep MemAvailable"""]
        
        shell_return_check_memory_available = subprocess.check_output(shell_command_check_memory_available, shell=True).decode('utf-8')

        system_memory_available = int(shell_return_check_memory_available.replace("MemAvailable:", "").replace(" kB", "").replace(" ", ""))

        return(200, system_memory_available)

    except subprocess.CalledProcessError:

        return([400])

#function to check total free memory
def check_system_memory_free():

    try:

        shell_command_check_memory_free = [F"""less /proc/meminfo | grep MemFree"""]
        
        shell_return_check_memory_free = subprocess.check_output(shell_command_check_memory_free, shell=True).decode('utf-8')

        system_memory_free = int(shell_return_check_memory_free.replace("MemFree:", "").replace(" kB", "").replace(" ", ""))

        return(200, system_memory_free)

    except subprocess.CalledProcessError:

        return([400])

#function to insert system load details into db
def insert_systemload_db(cpu_temperature_code, cpu_temperature, memory_type, memory_total_code, memory_total, memory_available_code, memory_available, memory_free_code, memory_free):

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

        insert_query = (f"INSERT INTO check_system_load (cpu_temperature_code, cpu_temperature, memory_type, memory_total_code, memory_total, memory_available_code, memory_available, memory_free_code, memory_free) VALUES ('{cpu_temperature_code}', '{cpu_temperature}', '{memory_type}', '{memory_total_code}', '{memory_total}', '{memory_available_code}', '{memory_available}', '{memory_free_code}', '{memory_free}')")
        
        cursor.execute(insert_query)

        conn.commit()
        
    except Exception as e:
        print(e)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()