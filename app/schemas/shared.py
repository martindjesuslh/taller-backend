from datetime import datetime
from pydantic import BaseModel


class SchemasBase(BaseModel):
    created_at: datetime
    updated_at: datetime
    id: int
