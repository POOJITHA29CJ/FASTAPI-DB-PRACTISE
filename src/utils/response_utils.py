from fastapi import *
def error_response(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)