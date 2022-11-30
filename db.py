import databases
import sqlalchemy
from decouple import config

DATABASE_URL = f"{config('DB_TYPE')}://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:{config('DB_PORT')}" \
               f"/{config('DB_TABLE')}"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
