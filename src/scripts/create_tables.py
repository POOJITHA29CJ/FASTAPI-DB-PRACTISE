from models.project import Project
from models.employee import Employee
from models.department import Department
from models.employee_project import Employee_project
from config import db
from peewee import *
def create_tables():
    with db:
        db.create_tables([
            Department,
            Employee,
            Project,
            Employee_project 
        ])
        print("Table created successfully")
if __name__=="__main__":
    create_tables()
    
