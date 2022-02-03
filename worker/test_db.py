# %%
import pandas as pd
from datetime import datetime as dt
import calendar
from sqlalchemy import create_engine
# import psycopg2 as pg
from pymongo import MongoClient
import motor.motor_asyncio
import pprint
import asyncio
import os


class DBOps():
    def __init__(self):
        MONGO_USER = os.environ.get('MONGO_USER')
        MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
        MONGO_HOST = os.environ.get('MONGO_HOST')
        MONGO_PORT = int(os.environ.get('MONGO_PORT'))
        POSTGRES_SERVER = os.environ.get('PGHOST')
        POSTGRES_USER = os.environ.get('PGUSER')
        POSTGRES_PASSWORD = os.environ.get('PGPASSWORD')
        POSTGRES_DB = os.environ.get('PGDATABASE')
        POSTGRES_PORT = os.environ.get('PGPORT')

        self.pg_conn = pg_conn = create_engine(
            f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
        )

        self.async_mongo_client = async_mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
            MONGO_HOST, MONGO_PORT, username=MONGO_USER, password=MONGO_PASSWORD)

        self.mongo_client = mongo_client = MongoClient(
            MONGO_HOST, MONGO_PORT, username=MONGO_USER, password=MONGO_PASSWORD)
        print(mongo_client.list_database_names())

    @classmethod
    def test_db(cls):
        cls.__init__(cls)
        print(cls.pg_conn.execute('SELECT datname FROM pg_database;').fetchall())
        print(cls.async_mongo_client.list_database_names())
        print(cls.mongo_client.list_database_names())


# %%
DBOps().test_db()


# %%


'''
db = client.shop
cars = db.cars
print(cars)


print(os.environ)
client = motor.motor_asyncio.AsyncIOMotorClient('mongo', 27017, username=os.environ.get(
    'MONGO_USER'), password=os.environ.get('MONGO_PASSWORD'))
print(await client.list_database_names())
client2 = MongoClient('mongo', 27017, username=os.environ.get(
    'MONGO_USER'), password=os.environ.get('MONGO_PASSWORD'))
print(client2.list_database_names())


POSTGRES_SERVER = os.environ.get('PGHOST')
POSTGRES_USER = os.environ.get('PGUSER')
POSTGRES_PASSWORD = os.environ.get('PGPASSWORD')
POSTGRES_DB = os.environ.get('PGDATABASE')
conn = create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}'
)
conn.execute('SELECT datname FROM pg_database;').fetchall()


async def do_find():
    cursor = cars.find()
    for document in await cursor.to_list(length=100):
        pprint.pprint(document)

if 1:
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(do_find())
    loop.create_task(do_find())

# seems like this is for threading
# asyncio.run(do_find())
client2 = MongoClient('localhost', 27017)
client2.shop.cars.find_one()

pd.options.display.max_columns = 500
pd.options.display.max_rows = 500
SPLYNX_KEY = '732479fe6245b1dc0527deb86504ddfd'
SPLYNX_SECRET = '4cd09707f2d98026b7d28e27f91c3b41'
SPLYNX_LOGIN = 'horizon_api'
SPLYNX_PASSWORD = 'D1g1t4lBl3nd'


class DataLoader():
    def __init__(self, local=True):

        if local:
            self.conn = create_engine(
                'postgresql://postgres:D1g1t4l500@db:5432/app')
        else:
            from helpers.config import settings
            POSTGRES_SERVER = settings.POSTGRES_SERVER
            POSTGRES_USER = settings.POSTGRES_USER
            POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
            POSTGRES_DB = settings.POSTGRES_DB
            self.conn = create_engine(
                f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5432/{POSTGRES_DB}'
            )
'''
