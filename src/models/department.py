from peewee import *
from models.base_model import BaseModel
class Department(BaseModel):
    department_id=AutoField()
    dep_name=CharField(max_length=100)
    dep_description=TextField(null=True)

