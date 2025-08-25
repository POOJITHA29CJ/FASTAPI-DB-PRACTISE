from pydantic import BaseModel
from datetime import date
class EmployeeProjectIn(BaseModel):
    employee_id:int
    project_id:int
    assigned_date:date
class EmployeeProjectOut(EmployeeProjectIn):
    pass