from peewee import *
from models.base_model import BaseModel
from models.department import Department
class Employee(BaseModel):
    employee_id=AutoField()
    emp_name=CharField(max_length=100)
    email=CharField(max_length=100,unique=True)
    phone=CharField(max_length=20)
    department_id=ForeignKeyField(Department,backref='employees',null=True)
    hire_date=DateField(null=True)
    salary=DecimalField(max_digits=10,decimal_places=2,null=True)