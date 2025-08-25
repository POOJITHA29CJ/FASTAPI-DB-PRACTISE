from pydantic import BaseModel
from typing import Optional
class DepartmentBase(BaseModel):
    dep_name:str
    dep_description:Optional[str]=None
class DepartmentCreate(DepartmentBase):
    pass
class DepartmentUpdate(BaseModel):
    dep_name:str
    dep_description:Optional[str]=None
class DepartmentOut(DepartmentBase):
    department_id:int