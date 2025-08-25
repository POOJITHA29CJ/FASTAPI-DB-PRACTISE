from fastapi import APIRouter, status
from models.project import Project
from schemas.project import ProjectIn, ProjectOut, ProjectUpdate
from playhouse.shortcuts import model_to_dict
from utils.logger import setup_logger
from utils.response_utils import error_response

router = APIRouter(prefix="/projects", tags=["Projects"])
logger = setup_logger()

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectIn):
    try:
        new_proj = Project.create(**project.dict())
        logger.info(f"Created new project with ID: {new_proj.project_id}")
        return model_to_dict(new_proj, recurse=False)
    except Exception as e:
        logger.error(f"Project creation failed: {e}")
        return error_response(status.HTTP_400_BAD_REQUEST, "Invalid input")

@router.get("/", response_model=list[ProjectOut], status_code=status.HTTP_200_OK)
def get_all_projects():
    try:
        projects = list(Project.select())
        logger.info(f"Fetched {len(projects)} project(s)")
        return [model_to_dict(p, recurse=False) for p in projects]
    except Exception as e:
        logger.error(f"Failed to fetch projects: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")

@router.get("/{id}", response_model=ProjectOut, status_code=status.HTTP_200_OK)
def get_project(id: int):
    try:
        proj = Project.get_by_id(id)
        logger.info(f"Fetched project with ID: {id}")
        return model_to_dict(proj, recurse=False)
    except Project.DoesNotExist:
        logger.warning(f"Project with ID {id} not found.")
        return error_response(status.HTTP_404_NOT_FOUND, "Project not found")
    except Exception as e:
        logger.error(f"Failed to fetch project {id}: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")

@router.put("/{id}", response_model=ProjectOut, status_code=status.HTTP_200_OK)
def update_project(id: int, update: ProjectUpdate):
    try:
        proj = Project.get_by_id(id)
        update_data = update.dict()
        for key, value in update_data.items():
            setattr(proj, key, value)
        proj.save()
        logger.info(f"Updated project with ID: {id}")
        return model_to_dict(proj, recurse=False)
    except Project.DoesNotExist:
        logger.warning(f"Update failed. Project with ID {id} not found.")
        return error_response(status.HTTP_404_NOT_FOUND, "Project not found")
    except Exception as e:
        logger.error(f"Project update failed for ID {id}: {e}")
        return error_response(status.HTTP_400_BAD_REQUEST, "Invalid input")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int):
    try:
        proj = Project.get_by_id(id)
        proj.delete_instance()
        logger.info(f"Deleted project with ID: {id}")
        return {"detail": "Project details deleted."}
    except Project.DoesNotExist:
        logger.warning(f"Delete failed. Project with ID {id} not found.")
        return error_response(status.HTTP_404_NOT_FOUND, "Project not found")
    except Exception as e:
        logger.error(f"Project deletion failed for ID {id}: {e}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")
