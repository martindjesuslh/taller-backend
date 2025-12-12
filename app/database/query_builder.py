from typing import Any, Optional, Tuple, List, Literal


class QueryBuilder:
    def __init__(self, schema: str, table: str):
        self.__table = f'"{schema}".{table}'
        self.__conditions: List[str] = []
        self.__insert_columns: List[str] = []
        self.__params: List[Any] = []
        self.__param_count = 1
        self.__select_fields = "*"
        self.__set_fields: List[str] = []
        self.__order_by_clause = ""
        self.__limit_clause = ""

    def select(self, *fields: str) -> "QueryBuilder":
        if fields:
            self.__select_fields = ", ".join(fields)
        return self

    def insert(self, **values) -> "QueryBuilder":
        for column, value in values.items():
            if value:
                self.__insert_columns.append(column)
                self.__params.append(value)

    def set(self, **fields) -> "QueryBuilder":
        for field, value in fields.items():
            if value is not None:
                self.__set_fields.append(f"{field} = ${self.__param_count}")
                self.__params.append(value)
                self.__param_count += 1

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
        self.__order_by_clause = f"ORDER BY {field} {direction}"
        return self

    def limit(self, limit: int, offset: int = 0) -> "QueryBuilder":
        self.__limit_clause = f"LIMIT {limit} OFFSET {offset}"
        return self

    def __build_where_clause(self) -> str:
        if self.__conditions:
            return "WHERE " + " AND ".join(self.__conditions)
        return ""

    def __build_set_clause(self) -> str:
        if self.__set_fields:
            return "SET " + ", ".join(self.__set_fields)
        return ""

    def __build_insert_clause(self) -> str:
        if self.__insert_columns:
            return "(" + ", ".join(self.__insert_columns) + ")"
        return ""

    def __build_select_query(self) -> str:
        where_clause = self.__build_where_clause()

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

    def __build_insert_values(self) -> "QueryBuilder":
        if self.__insert_columns:
            placeholders = [f"${i + 1}" for i in range(len(self.__insert_columns))]
            return "VALUES (" + " ,".join(placeholders) + ")"
        return ""

    def build_insert(self, returning: Optional[List[str]] = None) -> Tuple[str, Tuple]:
        columns_clause = self.__build_insert_clause()
        value_clause = self.__build_insert_values()

        if not columns_clause:
            raise ValueError("INSERT requerid at least one column")

        returning_clause = ""
        if returning:
            returning_clause = f"RETURNING {', '.join(returning)}"

        query = f"""
            INSERT INTO {self.__table} {columns_clause}
            {value_clause}
            {returning_clause}
        """

        return query, tuple(self.__params) if self.__params else None

    def build_update(
        self, returning: Optional[List[str]] = None
    ) -> Tuple[str, Optional[Tuple]]:
        set_clause = self.__build_set_clause()
        where_clause = self.__build_where_clause()

        if not set_clause:
            raise ValueError("UPDATE requires at least one field in SET clause")

        returning_clause = ""
        if returning:
            returning_clause = f"RETURNING {', '.join(returning)}"

        query = f"""
            UPDATE {self.__table}
            {set_clause}
            {where_clause}
            {returning_clause}
        """

        return query, tuple(self.__params) if self.__params else None
