import databases
import sqlalchemy
from decouple import config

DATABASE_URL = f"{config('DB_TYPE')}://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_ENDPOINT')}:{config('DB_PORT')}/{config('DB_NAME')}"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
