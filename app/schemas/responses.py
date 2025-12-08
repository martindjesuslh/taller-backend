from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: List[Dict[str, Any]] = Field(default_factory=list)
    status: int
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    @staticmethod
    def success(
        message: str,
        data: Optional[List[Dict[str, Any]]] = None,
        status_code: int = 200,
    ):
        return {
            "success": True,
            "message": message,
            "data": data or [],
            "status": status_code,
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def error(
        message: str,
        status_code: int = 400,
        errors: Optional[List[Dict[str, Any]]] = None,
    ):
        return {
            "success": False,
            "message": message,
            "status": status_code,
            "errors": errors,
        }


@staticmethod
def ok(message: str = "Success", data: Optional[List[Dict[str, Any]]] = None) -> dict:
    return ApiResponse.success(message, data, 200)


@staticmethod
def created(
    message: str = "Resource created successfully",
    data: Optional[List[Dict[str, Any]]] = None,
) -> dict:
    return ApiResponse.success(message, data, 201)


@staticmethod
def no_content(message: str = "Operation completed successfully") -> dict:
    return ApiResponse.success(message, [], 204)


# ===== ERROR HELPERS =====


@staticmethod
def bad_request(
    message: str = "Bad request", errors: Optional[List[Dict[str, Any]]] = None
) -> dict:
    return ApiResponse.error(message, 400, errors)


@staticmethod
def unauthorized(
    message: str = "Unauthorized", errors: Optional[List[Dict[str, Any]]] = None
) -> dict:
    return ApiResponse.error(message, 401, errors)


@staticmethod
def forbidden(
    message: str = "Forbidden", errors: Optional[List[Dict[str, Any]]] = None
) -> dict:
    return ApiResponse.error(message, 403, errors)


@staticmethod
def not_found(
    message: str = "Resource not found",
    errors: Optional[List[Dict[str, Any]]] = None,
) -> dict:
    return ApiResponse.error(message, 404, errors)


@staticmethod
def conflict(
    message: str = "Resource already exists",
    errors: Optional[List[Dict[str, Any]]] = None,
) -> dict:
    return ApiResponse.error(message, 409, errors)


@staticmethod
def internal_error(
    message: str = "Internal server error",
    errors: Optional[List[Dict[str, Any]]] = None,
) -> dict:
    return ApiResponse.error(message, 500, errors)
