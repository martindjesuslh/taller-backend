from typing import Any, Optional, Tuple, List, Literal


class QueryBuilder:
    def __init__(self, schema: str, table: str):
        self.__table = f'"{schema}".{table}'
        self.__conditions: List[str] = []
        self.__params: List[Any] = []
        self.__param_count = 1
        self.__select_fields = "*"
        self.__order_by_clause = ""
        self.__limit_clause = ""

    def select(self, *fields: str) -> "QueryBuilder":
        if fields:
            self.__select_fields = ", ".join(fields)
        return self

    def where(self, **filters) -> "QueryBuilder":
        for field, value in filters.items():
            if value is not None:
                self.__conditions.append(f"{field} = ${self.__param_count}")
                self.__params.append(value)
                self.__param_count += 1
        return self

    def order_by(
        self, field: str, direction: Literal["ASC", "DESC"] = "ASC"
    ) -> "QueryBuilder":
        self.__order_by_clause = f" ORDER BY {field} {direction}"
        return self

    def limit(self, limit: int, offset: int = 0) -> "QueryBuilder":
        self.__limit_clause = f"LIMIT {limit} OFFSET {offset}"
        return self

    def __build_where_where(self) -> str:
        if self.__conditions:
            return "WHERE " + " AND ".join(self.__conditions)
        return ""

    def __build_select_query(self) -> str:
        where_clause = self.__build_where_where()

        query = f"""
            SELECT {self.__select_fields}
            FROM {self.__table} 
            {where_clause}
            {self.__order_by_clause}
            {self.__limit_clause}
        """.strip()

        return query

    def build_select(self) -> Tuple[str, Optional[Tuple]]:
        query = self.__build_select_query()
        return query, tuple(self.__params) if self.__params else None
