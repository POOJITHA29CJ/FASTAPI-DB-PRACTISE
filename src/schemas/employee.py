from pydantic import BaseModel
from typing import Optional
from datetime import date
class EmployeeIn(BaseModel):
    emp_name:str
    email:str
    phone:str
    department_id:int
    hire_date:date
    salary:float
class EmployeeUpdate(BaseModel):
    emp_name:Optional[str]
    email:Optional[str]=None
    phone:Optional[str]=None
    department_id:Optional[int]=None
    hire_date:Optional[date]=None
    salary:Optional[float]=None
class EmployeeOut(EmployeeIn):
    employee_id:int

