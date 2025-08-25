from peewee import *
from config import db
class BaseModel(Model):
    class Meta:
        database=db
