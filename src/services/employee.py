from peewee import *
from fastapi import APIRouter, HTTPException, status
from typing import List
from playhouse.shortcuts import model_to_dict
from models.employee import Employee
from schemas.employee import EmployeeIn, EmployeeOut, EmployeeUpdate
from utils.logger import setup_logger
from utils.response_utils import error_response

logger = setup_logger()
router = APIRouter(prefix="/employee", tags=["Employee"])

@router.get("/", response_model=List[EmployeeOut], status_code=status.HTTP_200_OK)
async def get_employee():
    try:
        employees = Employee.select()
        if not employees:
            logger.warning("No employees found.")
            return error_response(status.HTTP_404_NOT_FOUND, "No employees found")
        logger.info("Fetched all employee records.")
        return [model_to_dict(emp, recurse=False) for emp in employees]
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")

@router.get("/{id}", response_model=EmployeeOut, status_code=status.HTTP_200_OK)
async def get_emp_id(id: int):
    try:
        employee = Employee.get_by_id(id)
        logger.info(f"Fetched employee with ID: {id}")
        return model_to_dict(employee, recurse=False)
    except Employee.DoesNotExist:
        logger.warning(f"Employee with ID {id} not found.")
        return error_response(status.HTTP_404_NOT_FOUND, "Employee not found")
    except Exception as e:
        logger.error(f"Error fetching employee {id}: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")

@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
async def create_employee(emp: EmployeeIn):
    try:
        new_emp = Employee.create(**emp.dict())
        logger.info(f"Created employee with ID: {new_emp.employee_id}")
        return model_to_dict(new_emp, recurse=False)
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        return error_response(status.HTTP_400_BAD_REQUEST, "Invalid employee data")

@router.put("/{id}", response_model=EmployeeOut)
def update_employee(id: int, emp_update: EmployeeUpdate):
    try:
        emp = Employee.get_by_id(id)
        update_data = emp_update.dict() 
        for key, value in update_data.items():
            setattr(emp, key, value)
        emp.save()
        return model_to_dict(emp, recurse=False)
    except Employee.DoesNotExist:
        raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid input")
    
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_employee(id: int):
    try:
        emp = Employee.get_by_id(id)
        emp.delete_instance()
        logger.info(f"Deleted employee with ID: {id}")
        return {"detail": "Employee deleted"}
    except Employee.DoesNotExist:
        logger.warning(f"Delete failed. Employee with ID {id} not found.")
        return error_response(status.HTTP_404_NOT_FOUND, "Employee not found")
    except Exception as e:
        logger.error(f"Error deleting employee {id}: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")

@router.patch("/{id}", response_model=EmployeeOut)
async def patch_employee(id: int, emp_update: EmployeeUpdate):
    try:
        emp = Employee.get_by_id(id)
        existing_data = model_to_dict(emp, recurse=False)
        patch_data = emp_update.dict(exclude_unset=True)

        if not patch_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided to update"
            )
        existing_data.update(patch_data)
        for key, value in existing_data.items():
            if hasattr(emp, key):  
                setattr(emp, key, value)

        emp.save()
        return EmployeeOut(**model_to_dict(emp, recurse=False))

    except Employee.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    except Exception as e:
        logger.error(f"Error updating employee {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input"
        )
