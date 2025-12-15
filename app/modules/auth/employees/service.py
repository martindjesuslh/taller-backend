from typing import Optional

from app.database.query_manager import QueryManager
from app.database.query_builder import QueryBuilder
from app.schemas.responses import ApiResponse
from app.schemas.employees import CreateEmployeeSchema, UpdateEmployeeSchema


class EmployeeService:
    def __init__(self):
        self.qm = QueryManager()

    async def get(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ):
        qb = QueryBuilder("user", "employees")

        qb.select()
        qb.where(email=email, phone=phone, is_active=True)
        qb.where_like(first_name=first_name, last_name=last_name)
        query, params = qb.build_select()

        data = await self.qm.select(query, params)

        return (
            ApiResponse.ok(data=data) if data else ApiResponse.no_content("Not found")
        )

    async def create(self, payload: CreateEmployeeSchema):
        qb = QueryBuilder("user", "employees")
        qb.insert(**payload.model_dump())
        query, params = qb.build_insert()

        await self.qm.write(query, params)

        return ApiResponse.created("User created")

    async def update(self, payload: UpdateEmployeeSchema):
        qb = QueryBuilder("user", "employees")
        qb.set(**payload.model_dump())
        query, params = qb.build_update(["*"])

        data = await self.qm.write(query, params, True)
        print("=" * 80, query)

        return ApiResponse.ok("The employee upload successfully", data)
