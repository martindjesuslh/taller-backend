from datetime import datetime, date
from typing import Any, List, Dict


def serialize_value(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def serialize_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not data:
        return []

    return [
        {key: serialize_value(value) for key, value in record.items()} for record in data
    ]
