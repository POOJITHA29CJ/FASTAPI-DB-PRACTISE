from peewee import *
from models.base_model import BaseModel
from models.employee import Employee
from models.project import Project
class Employee_project(BaseModel):
    employee_id=ForeignKeyField(Employee,backref='projects')
    project_id=ForeignKeyField(Project,backref='employees')
    assigned_date=DateField()
    class Meta:
        primary_key=CompositeKey('employee_id', 'project_id')