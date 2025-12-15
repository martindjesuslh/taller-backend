from fastapi import APIRouter, Query
from typing import Optional

from app.schemas.employees import CreateEmployeeSchema, UpdateEmployeeSchema
from app.modules.auth.employees.service import EmployeeService

router = APIRouter()


@router.get("")
async def get_employees(
    first_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
):
    service = EmployeeService()

    return await service.get(first_name, last_name, email, phone)


@router.post("")
async def create_employee(payload: CreateEmployeeSchema):
    service = EmployeeService()

    return await service.create(payload)


@router.put("")
async def upload_employee(payload: UpdateEmployeeSchema):
    service = EmployeeService()

    return await service.update(payload)
