from models.employee_project import Employee_project
from models.employee import Employee
from models.project import Project
from playhouse.shortcuts import model_to_dict
from schemas.employee_project import EmployeeProjectIn, EmployeeProjectOut
from typing import List
from fastapi import APIRouter, HTTPException, status
from utils.logger import setup_logger
from utils.response_utils import error_response

router = APIRouter(prefix="/employee-project", tags=["EmployeeProject"])
logger = setup_logger()

@router.get("/", response_model=List[EmployeeProjectOut], status_code=status.HTTP_200_OK)
def get_all_assignments():
    try:
        assignments = Employee_project.select()
        logger.info(f"Fetched {len(assignments)} assignments.")
        return [
            model_to_dict(a, recurse=False, only=[
                Employee_project.employee_id,
                Employee_project.project_id,
                Employee_project.assigned_date
            ]) for a in assignments
        ]
    except Exception as e:
        logger.error(f"Error fetching assignments: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch assignments.")

@router.post("/", response_model=EmployeeProjectOut, status_code=status.HTTP_201_CREATED)
def assign_employee_to_project(data: EmployeeProjectIn):
    try:
        assignment = Employee_project.create(**data.dict())
        logger.info(f"Assigned employee {assignment.employee_id} to project {assignment.project_id}")
        return model_to_dict(assignment,recurse=False)
    except Exception as e:
        logger.error(f"Assignment failed: {e}")
        return error_response(status.HTTP_400_BAD_REQUEST, "Assignment failed")

@router.get("/project/{project_id}", response_model=List[EmployeeProjectOut], status_code=status.HTTP_200_OK)
def get_assignments_by_project(project_id: int):
    try:
        assignments = Employee_project.select().where(Employee_project.project_id == project_id)
        logger.info(f"Fetched assignments for project ID: {project_id}")
        return [
            model_to_dict(a, recurse=False, only=[
                Employee_project.project_id,
                Employee_project.assigned_date,
                Employee_project.employee_id
            ]) for a in assignments
        ]
    except Exception as e:
        logger.error(f"Error fetching assignments for project {project_id}: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error fetching project assignments")

@router.get("/employee/{employee_id}", response_model=List[EmployeeProjectOut], status_code=status.HTTP_200_OK)
def get_assignments_by_employee(employee_id: int):
    try:
        assignments = Employee_project.select().where(Employee_project.employee_id == employee_id)
        logger.info(f"Fetched assignments for employee ID: {employee_id}")
        return [
            model_to_dict(a, recurse=False, only=[
                Employee_project.employee_id,
                Employee_project.project_id,
                Employee_project.assigned_date
            ]) for a in assignments
        ]
    except Exception as e:
        logger.error(f"Error fetching assignments for employee {employee_id}: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error fetching employee assignments")

@router.get("/project/{project_id}/employees", response_model=List[dict], status_code=status.HTTP_200_OK)
def get_employee_names_by_project(project_id: int):
    try:
        assignments = (
            Employee_project.select(Employee_project, Employee)
            .join(Employee)
            .where(Employee_project.project_id == project_id)
        )
        assignments_list = list(assignments)

        if not assignments_list:
            logger.warning(f"No employees found for project ID: {project_id}")
            return error_response(status.HTTP_404_NOT_FOUND, "No employees found for this project.")

        logger.info(f"Fetched employees for project ID: {project_id}")
        return [
            {
                "employee_id": a.employee_id.employee_id,
                "employee_name": a.employee_id.emp_name,
                "assigned_date": a.assigned_date
            }
            for a in assignments_list
        ]
    except Exception as e:
        logger.error(f"Error fetching employees for project {project_id}: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error fetching employee details")

@router.get("/employee/{employee_id}/projects", response_model=List[dict], status_code=status.HTTP_200_OK)
def get_project_names_by_employee(employee_id: int):
    try:
        assignments = (
            Employee_project.select(Employee_project, Project)
            .join(Project)
            .where(Employee_project.employee_id == employee_id)
        )
        assignments_list = list(assignments)

        if not assignments_list:
            logger.warning(f"No projects found for employee ID: {employee_id}")
            return error_response(status.HTTP_404_NOT_FOUND, "No projects found for this employee.")

        logger.info(f"Fetched projects for employee ID: {employee_id}")
        return [
            {
                "project_id": a.project_id.project_id,
                "project_name": a.project_id.project_name,
                "project_description": a.project_id.description
            }
            for a in assignments_list
        ]
    except Exception as e:
        logger.error(f"Error fetching projects for employee {employee_id}: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error fetching project details")
