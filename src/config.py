from peewee import MySQLDatabase
from dotenv import load_dotenv
import os
load_dotenv()
db=MySQLDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT'))
)
