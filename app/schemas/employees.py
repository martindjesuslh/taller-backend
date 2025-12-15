from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from .shared import SchemasBase


class EmployeeBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=20,
    )
    address: Optional[str] = Field(default=None, min_length=3, max_length=255)
    is_active: bool = True
    password: str = Field(min_length=8, max_length=255)
    role_id: int = Field(min=1)


class CreateEmployeeSchema(EmployeeBase):
    pass


class UpdateEmployeeSchema(EmployeeBase):
    id: int


class EmployeeSchema(SchemasBase, EmployeeBase):
    pass
