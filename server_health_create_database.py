from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from dotenv import dotenv_values, load_dotenv
import os

load_dotenv()

db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_port_id = os.getenv("db_port_id")
db_hostname = os.getenv("db_hostname")
db_user = os.getenv("db_user")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

inspection = inspect(engine)

Base = declarative_base()

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

if table_2_check == False:
    print(f"'{table_2_name}' = missing, attempting to create table.")

    class check_ongoing_processes(Base):
        __tablename__ = table_2_name
        id = Column(BigInteger, primary_key=True, nullable=False)
        timestamp_log = Column(DateTime(timezone=False), server_default=func.now())
        process_name = Column(String(30), nullable=False)
        process_pass_fail = Column(String(4), nullable=False)

    Base.metadata.create_all(engine)