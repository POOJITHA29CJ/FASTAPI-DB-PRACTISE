from pydantic import BaseModel
from datetime import date
from typing import Optional

class ProjectIn(BaseModel):
    project_name: str
    description: str
    start_date: date
    end_date: Optional[date] = None

class ProjectOut(ProjectIn):
    project_id: int

class ProjectUpdate(BaseModel):
    project_name: Optional[str]=None
    description: Optional[str]=None
    start_date: Optional[date]=None
    end_date: Optional[date]=None
    
