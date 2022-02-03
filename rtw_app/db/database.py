from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


class Databases():
    def __init__(self):
        if not os.environ.get('MONGO_HOST'):
            from dotenv import load_dotenv
            from pathlib import Path
            #dotenv_path = Path(LOCAL_ENV_PATH)
            load_dotenv(os.path.join(BASE_DIR, ".env"))
            sys.path.append(BASE_DIR)
            os.environ['PGHOST'] = 'localhost'
            os.environ['MONGO_HOST'] = 'localhost'

        MONGO_USER = os.environ.get('MONGO_USER')
        MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
        MONGO_HOST = os.environ.get('MONGO_HOST')
        MONGO_PORT = int(os.environ.get('MONGO_PORT'))
        POSTGRES_SERVER = os.environ.get('PGHOST')
        POSTGRES_USER = os.environ.get('PGUSER')
        POSTGRES_PASSWORD = os.environ.get('PGPASSWORD')
        POSTGRES_DB = os.environ.get('PGDATABASE')
        POSTGRES_PORT = os.environ.get('PGPORT')

        SQLITE_DATABASE_URL = 'sqlite:///./ig_api.db'
        self.sqlite_conn = create_engine(SQLITE_DATABASE_URL, connect_args={
            "check_same_thread": False})

        self.pg_conn = pg_conn = create_engine(
            f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
        )
        self.SQLITE_SessionLocal = sessionmaker(
            bind=self.sqlite_conn, autocommit=False, autoflush=False)
        self.PSQL_SessionLocal = sessionmaker(
            bind=self.pg_conn, autocommit=False, autoflush=False)

        self.async_mongo_client = async_mongo_client = AsyncIOMotorClient(
            MONGO_HOST, MONGO_PORT, username=MONGO_USER, password=MONGO_PASSWORD)

        self.mongo_client = mongo_client = MongoClient(
            MONGO_HOST, MONGO_PORT, username=MONGO_USER, password=MONGO_PASSWORD)
        #print(MONGO_USER, MONGO_PASSWORD)
        print(mongo_client.list_database_names())
        print(pg_conn.execute('SELECT datname FROM pg_database;').fetchall())

    @classmethod
    def test_db(cls):
        cls.__init__(cls)
        print(cls.pg_conn.execute('SELECT datname FROM pg_database;').fetchall())
        print(cls.async_mongo_client.list_database_names())
        print(cls.mongo_client.list_database_names())


databases = Databases()
Base = declarative_base()


def get_psql():
    db = databases.PSQL_SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_sqlite():
    db = databases.SQLITE_SessionLocal()

    try:
        yield db
    finally:
        db.close()
