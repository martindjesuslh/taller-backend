from typing import Optional
from pydantic import BaseModel, Field

from .shared import SchemasBase


class RoleBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = True


class CreateRole(RoleBase):
    pass


class UpdateRole(RoleBase):
    id: int


class RolSchema(SchemasBase, RoleBase):
    pass
