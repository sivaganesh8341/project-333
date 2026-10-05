from fastapi.responses import JSONResponse
from fastapi import status, Request
from .custom_exceptions import DuplicateNameException, NotFoundException

def duplicate_name_exception_handler(request: Request, exc: DuplicateNameException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": f"The name '{exc.name}' already exists.", "status_code": 400},
    )

def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"{exc.name} not found", "status_code": 404},
    )

def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "An unexpected error occurred.", "details": str(exc), "status_code": 500},
    )
