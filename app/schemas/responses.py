from datetime import datetime
from typing import Optional, List, Dict, Any, Callable

from fastapi.responses import JSONResponse
from app.utils.serializers import serialize_data

TData = Optional[List[Dict[str, Any]]]


class ApiResponse:
    @staticmethod
    def success(
        message: str,
        data: TData = None,
        status_code: int = 200,
    ) -> JSONResponse:
        content = {
            "success": True,
            "message": message,
            "data": serialize_data(data) if data else [],
            "status": status_code,
            "timestamp": datetime.now().isoformat(),
        }

        return JSONResponse(content=content, status_code=status_code)

    @staticmethod
    def error(
        message: str,
        errors: TData = None,
        status_code: int = 400,
    ) -> JSONResponse:
        detail = {
            "success": False,
            "message": message,
            "status": status_code,
            "errores": errors,
            "timestamp": datetime.now().isoformat(),
        }

        return JSONResponse(status_code=status_code, content=detail)

    @staticmethod
    def ok(message: str = "Success", data: TData = None) -> JSONResponse:
        return ApiResponse.success(message, data, 200)

    @staticmethod
    def created(
        message: str = "Resource created successfully",
        data: TData = None,
    ) -> JSONResponse:
        return ApiResponse.success(message, data, 201)

    @staticmethod
    def no_content(
        message: str = "Operation completed successfully", data: TData = None
    ) -> JSONResponse:
        return ApiResponse.success(message, data, 204)

    @staticmethod
    def bad_request(message: str = "Bad request", errors: TData = None) -> JSONResponse:
        return ApiResponse.error(message, errors, 400)

    @staticmethod
    def unauthorized(
        message: str = "Unauthorized", errors: TData = None
    ) -> JSONResponse:
        return ApiResponse.error(message, errors, 401)

    @staticmethod
    def forbidden(message: str = "Forbidden", errors: TData = None) -> JSONResponse:
        return ApiResponse.error(message, errors, 403)

    @staticmethod
    def not_found(
        message: str = "Resource not found",
        errors: TData = None,
    ) -> JSONResponse:
        return ApiResponse.error(message, errors, 404)

    @staticmethod
    def conflict(
        message: str = "Resource already exists",
        errors: TData = None,
    ) -> JSONResponse:
        return ApiResponse.error(message, errors, 409)

    @staticmethod
    def internal_error(
        message: str = "Internal server error",
        errors: TData = None,
    ) -> JSONResponse:
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
    message: Optional[str] = None,
    data: TData = None,
    errors: TData = None,
) -> JSONResponse:
    func = STATUS_MAP.get(status_code)

    if not func:
        if status_code >= 200 and status_code < 300:
            return ApiResponse.success(message or "Success", status_code, data)
        return ApiResponse.error(message or "An error occurred", status_code, errors)

    if status_code < 400:
        return func(message, data) if message else func(data=data)

    return func(message, errors) if message else func(errors=errors)
