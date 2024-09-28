from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date, Float
from sqlalchemy.dialects.postgresql import CIDR
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

inspection = inspect(engine)

Base = declarative_base()

#create first required table
table_1_name = "server_identities"
table_1_check = inspection.has_table(table_1_name)

if table_1_check == False:
    print(f"'{table_1_name}' = missing, attempting to create table.")

    class list_localhost_ongoing_processes(Base):
        __tablename__ = table_1_name
        server_name = Column(String(30), primary_key=True, nullable=False)
        server_ip_address = Column(CIDR, unique=True)

    Base.metadata.create_all(engine)

#create second required table
table_2_name = "check_ping_response"
table_2_check = inspection.has_table(table_2_name)

if table_2_check == False:
    print(f"'{table_2_name}' = missing, attempting to create table.")

    class list_localhost_ongoing_processes(Base):
        __tablename__ = table_2_name
        id = Column(BigInteger, primary_key=True, nullable=False)
        timestamp_log = Column(DateTime(timezone=False), server_default=func.now())
        server_ip_address = Column(CIDR, nullable=False)
        ping_pass_fail = Column(String(4), nullable=False)

    Base.metadata.create_all(engine)

#create third required table
table_3_name = "server_database_credentials"
table_3_check = inspection.has_table(table_3_name)

if table_3_check == False:
    print(f"'{table_3_name}' = missing, attempting to create table.")

    class list_localhost_ongoing_processes(Base):
        __tablename__ = table_3_name
        timestamp_added = Column(DateTime(timezone=False), server_default=func.now())
        server_ip_address = Column(CIDR, primary_key=True, nullable=False)
        server_ip_address_text = Column(String(15), nullable=False)
        server_database = Column(String(25), primary_key=True, nullable=False)
        server_username = Column(String(10), nullable=False)
        server_password = Column(String(30), nullable=False)
        server_port = Column(Integer, nullable=False)

    Base.metadata.create_all(engine)

#create fourth required table
table_4_name = "cs_server_health_api_keys"
table_4_check = inspection.has_table(table_4_name)

if table_4_check == False:
    print(f"'{table_4_name}' = missing, attempting to create table.")

    class list_localhost_ongoing_processes(Base):
        __tablename__ = table_4_name
        timestamp_added = Column(DateTime(timezone=False), server_default=func.now())
        api_key = Column(String(32), primary_key=True, unique=True, nullable=False)
        username = Column(String(15), primary_key=True, nullable=False)
        access_read = Column(Integer, nullable=False)
        access_write = Column(Integer, nullable=False)
        access_update = Column(Integer, nullable=False)
        access_delete = Column(Integer, nullable=False)

    Base.metadata.create_all(engine)