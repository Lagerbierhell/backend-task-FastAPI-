from databases import Database
from sqlalchemy import MetaData, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

ASYNC_DATABASE_URL = os.getenv("DATABASE_URL","") ## Wenn die .env datenbank nicht klappt
database = Database(ASYNC_DATABASE_URL)

SYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("+asyncpg", "")
sync_engine = create_engine(SYNC_DATABASE_URL)

metadata = MetaData()

