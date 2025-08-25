from peewee import *
from models.base_model import BaseModel
class Project(BaseModel):
    project_id=AutoField()
    project_name=CharField(max_length=100)
    description=TextField(null=True)
    start_date=DateField(null=True)
    end_date=DateField(null=True)
