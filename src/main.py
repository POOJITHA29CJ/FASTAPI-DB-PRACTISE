from fastapi import FastAPI
from services import department,employee,project,employee_project
app=FastAPI(title="Employee Management system")
app.include_router(department.router)
app.include_router(employee.router)
app.include_router(project.router)
app.include_router(employee_project.router)