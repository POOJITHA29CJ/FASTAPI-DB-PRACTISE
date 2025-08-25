from fastapi import APIRouter,status
from peewee import *
from typing import List
from playhouse.shortcuts import model_to_dict
from models.department import Department
from schemas.department import DepartmentOut, DepartmentCreate, DepartmentUpdate
from utils.logger import setup_logger
from utils.response_utils import error_response
logger = setup_logger()
router = APIRouter(prefix="/departments", tags=["Department"])

@router.get("/", response_model=List[DepartmentOut],status_code=status.HTTP_200_OK)
async def get_department():
    departments = list(Department.select())
    if not departments:
        logger.warning("No department records found.")
        return error_response(status.HTTP_404_NOT_FOUND, "Department not found")
    logger.info("Fetched all department records.")
    return [model_to_dict(dep) for dep in departments]

@router.get("/{department_id}", response_model=DepartmentOut,status_code=status.HTTP_200_OK)
async def get_department_by_id(department_id: int):
    try:
        department = Department.get(Department.department_id == department_id)
        logger.info(f"Fetched department with ID: {department_id}")
        return model_to_dict(department)
    except Department.DoesNotExist:
        logger.warning(f"Department with ID {department_id} not found.")
        return error_response(status.HTTP_404_NOT_FOUND, "Department not found")

@router.post("/", response_model=DepartmentOut, status_code=201)
async def create_department(dep: DepartmentCreate):
    try:
      department = Department.create(**dep.dict())
      logger.info(f"Created new department with ID: {department.department_id}")
      return model_to_dict(department)
    except Exception as e:
      logger.error(f"Department creation failed: {e}")
      return error_response(status.HTTP_400_BAD_REQUEST, "Invalid department data")

@router.put("/{id}", response_model=DepartmentOut,status_code=status.HTTP_200_OK)
async def update_department(id: int, dep: DepartmentUpdate):
    try:
        department = Department.get_by_id(id)
        dep_data = dep.dict()
        for key, value in dep_data.items():
            setattr(department, key, value)
        department.save()
        logger.info(f"Updated department with ID: {id}")
        return model_to_dict(department)
    except Department.DoesNotExist:
        logger.warning(f"Update failed. Department with ID {id} not found.")
        return error_response(status.HTTP_404_NOT_FOUND,"Department not found")
    except Exception as e:
        logger.error(f"Department update failed: {e}")
        return error_response(status.HTTP_400_BAD_REQUEST, "Invalid update data")

@router.delete("/{id}",status_code=status.HTTP_200_OK)
def delete_department(id: int):
    try:
        department = Department.get_by_id(id)
        department.delete_instance()
        logger.info(f"Deleted department with ID: {id}")
        return {"detail": "Department deleted."}
    except Department.DoesNotExist:
        logger.warning(f"Delete failed. Department with ID {id} not found.")
        return error_response(status.HTTP_404_NOT_FOUND, "Department not found")
    except Exception as e:
        logger.error(f"Department deletion failed: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")
