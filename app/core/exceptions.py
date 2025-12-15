import asyncpg
from traceback import extract_tb
from fastapi import Request

from app.schemas.responses import from_status

DB_EXCEPTION_MAP = {
    asyncpg.UniqueViolationError: 409,
    asyncpg.ForeignKeyViolationError: 409,
    asyncpg.NotNullViolationError: 400,
    asyncpg.CheckViolationError: 400,
}


def _get_status_code(exc: Exception) -> int:
    for exc_type, code in DB_EXCEPTION_MAP.items():
        if isinstance(exc, exc_type):
            return code

    return 500


async def global_exception_handler(request: Request, exc: Exception):
    tb = extract_tb(exc.__traceback__)

    app_frames = [
        frame
        for frame in tb
        if "/app/" in frame.filename and "site-packages" not in frame.filename
    ]

    print("\n" + "=" * 80)
    print(f"ERROR in {request.method} {request.url.path}")
    print("=" * 80)

    if app_frames:
        last_frame = app_frames[-1]
        file_path = last_frame.filename.split("/app/")[-1]

        print(f"File: {file_path}:{last_frame.lineno}")
        print(f"Function: {last_frame.name}")
        print(f"Line: {last_frame.line}")

    error_msg = str(exc)
    print(f"Error: {type(exc).__name__}: {error_msg}")
    print("=" * 80 + "\n" + error_msg)

    status_code = _get_status_code(exc)

    return from_status(status_code)
