from datetime import datetime
from typing import Optional, List, Dict, Any, Callable
from fastapi import HTTPException
from fastapi.responses import JSONResponse


class ApiResponse:
    success: bool
    message: str
    data: List[Dict[str, Any]] = None
    error_message: Optional[str] = None
    status: int

    @staticmethod
    def success(
        message: str,
        data: Optional[List[Dict[str, Any]]] = None,
        status_code: int = 200,
    ):
        content = {
            "success": True,
            "message": message,
            "data": data or [],
            "status": status_code,
            "timestamp": datetime.now().isoformat(),
        }

        return JSONResponse(content=content, status_code=status_code)

    @staticmethod
    def error(
        message: str,
        error_message: str,
        status_code: int = 400,
    ):
        detail = {
            "success": False,
            "message": message,
            "status": status_code,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat(),
        }

        raise HTTPException(status_code=status_code, detail=detail)

    @staticmethod
    def ok(
        message: str = "Success", data: Optional[List[Dict[str, Any]]] = None
    ) -> dict:
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

    @staticmethod
    def bad_request(
        message: str = "Bad request", errors: Optional[List[Dict[str, Any]]] = None
    ) -> dict:
        return ApiResponse.error(message, errors, 400)

    @staticmethod
    def unauthorized(
        message: str = "Unauthorized", errors: Optional[List[Dict[str, Any]]] = None
    ) -> dict:
        return ApiResponse.error(message, errors, 401)

    @staticmethod
    def forbidden(
        message: str = "Forbidden", errors: Optional[List[Dict[str, Any]]] = None
    ) -> dict:
        return ApiResponse.error(message, errors, 403)

    @staticmethod
    def not_found(
        message: str = "Resource not found",
        errors: Optional[List[Dict[str, Any]]] = None,
    ) -> dict:
        return ApiResponse.error(message, errors, 404)

    @staticmethod
    def conflict(
        message: str = "Resource already exists",
        errors: Optional[List[Dict[str, Any]]] = None,
    ) -> dict:
        return ApiResponse.error(message, errors, 409)

    @staticmethod
    def internal_error(
        message: str = "Internal server error",
        errors: Optional[List[Dict[str, Any]]] = None,
    ) -> dict:
        return ApiResponse.error(message, errors, 500)


STATUS_MAP: Dict[int, Callable] = {
    200: ApiResponse.ok,
    201: ApiResponse.created,
    204: ApiResponse.no_content,
    400: ApiResponse.bad_request,
    401: ApiResponse.unauthorized,
    403: ApiResponse.forbidden,
    404: ApiResponse.not_found,
    409: ApiResponse.conflict,
    500: ApiResponse.internal_error,
}


def from_status(
    status_code: int,
    message: str,
    data: Optional[List[Dict[str, Any]]] = None,
    error_message: Optional[List[Dict[str, Any]]] = None,
):
    if status_code in STATUS_MAP:
        func = STATUS_MAP[status_code]

        if status_code < 400:
            return func(message, data)
        else:
            return func(message, error_message)

    if status_code >= 200 and status_code < 300:
        return ApiResponse.success(message, data, status_code)
    else:
        return ApiResponse.error(message, error_message or "Unknown error", status_code)
