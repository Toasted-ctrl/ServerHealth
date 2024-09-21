from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date, Float
from dotenv import dotenv_values, load_dotenv
import os

#import dotenv values
load_dotenv()

db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_port_id = os.getenv("db_port_id")
db_hostname = os.getenv("db_hostname")
db_user = os.getenv("db_user")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

#create engine to connect to db
engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

#inspect database using engine to check for table presence
inspection = inspect(engine)

Base = declarative_base()

#block to create first table required
table_1_name = "list_localhost_ongoing_processes"
table_1_check = inspection.has_table(table_1_name)

if table_1_check == False:
    print(f"'{table_1_name}' = missing, attempting to create table.")

    class list_localhost_ongoing_processes(Base):
        __tablename__ = table_1_name
        process_name = Column(String(30), primary_key=True, nullable=False)
        process_date_added = Column(Date, nullable=False)

    Base.metadata.create_all(engine)

table_2_name = "check_ongoing_processes"
table_2_check = inspection.has_table(table_2_name)

#block to create second table required
if table_2_check == False:
    print(f"'{table_2_name}' = missing, attempting to create table.")

    class check_ongoing_processes(Base):
        __tablename__ = table_2_name
        id = Column(BigInteger, primary_key=True, nullable=False)
        timestamp_log = Column(DateTime(timezone=False), server_default=func.now())
        process_name = Column(String(30), nullable=False)
        process_pass_fail = Column(String(4), nullable=False)

    Base.metadata.create_all(engine)

#block to create third table required
table_3_name = "check_system_load"
table_3_check = inspection.has_table(table_3_name)

if table_3_check == False:
    print(f"'{table_3_name}' = missing, attempting to create table.")

    class check_ongoing_processes(Base):
        __tablename__ = table_3_name
        id = Column(BigInteger, primary_key=True, nullable=False)
        timestamp_log = Column(DateTime(timezone=False), server_default=func.now())
        cpu_temperature_code = Column(Integer, nullable=False)
        cpu_temperature = Column(Float, nullable=False)
        memory_type = Column(String(8), nullable=False)
        memory_total_code = Column(Integer, nullable=False)
        memory_total = Column(Integer, nullable=False)
        memory_available_code = Column(Integer, nullable=False)
        memory_available = Column(Integer, nullable=False)
        memory_free_code = Column(Integer, nullable=False)
        memory_free = Column(Integer, nullable=False)

    Base.metadata.create_all(engine)

#block to create fourth table required
table_4_name = "database_table_load_frequency"
table_4_check = inspection.has_table(table_4_name)

if table_4_check == False:
    print(f"'{table_4_name}' = missing, attempting to create table.")

    class check_ongoing_processes(Base):
        __tablename__ = table_4_name
        timestamp_log = Column(DateTime(timezone=False), server_default=func.now())
        database_name = Column(String(30), primary_key=True, nullable=False)
        table_name = Column(String(40), primary_key=True, nullable=False)
        load_frequency_hours = Column(Integer, nullable=False)

    Base.metadata.create_all(engine)