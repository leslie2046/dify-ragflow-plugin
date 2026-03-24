import json
import importlib
from typing import Any


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if item not in (None, "")]
    if isinstance(value, tuple):
        return [item for item in value if item not in (None, "")]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [value]


def require_list(value: Any, parameter_name: str) -> list[Any]:
    items = ensure_list(value)
    if not items:
        raise ValueError(f"{parameter_name} is required")
    return items


def normalize_result(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize_result(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_result(item) for item in value]
    if isinstance(value, tuple):
        return [normalize_result(item) for item in value]
    to_json = getattr(value, "to_json", None)
    if callable(to_json):
        return normalize_result(to_json())
    if hasattr(value, "__dict__"):
        return {
            key: normalize_result(item)
            for key, item in vars(value).items()
            if key != "rag" and not key.startswith("_") and not callable(item)
        }
    return value


def memory_to_json(memory: Any) -> dict[str, Any]:
    return normalize_result(memory)


def require_memory(memories: list[Any], memory_id: str) -> Any:
    for memory in memories:
        if getattr(memory, "id", None) == memory_id:
            return memory
    raise ValueError(f"Memory with ID {memory_id} not found")


def parse_json_object(value: str, parameter_name: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{parameter_name} must be valid JSON") from exc

    if not isinstance(parsed, dict):
        raise ValueError(f"{parameter_name} must be a JSON object")

    return parsed


def require_string(value: Any, parameter_name: str) -> str:
    if value is None:
        raise ValueError(f"{parameter_name} is required")

    text = str(value).strip()
    if not text:
        raise ValueError(f"{parameter_name} is required")

    return text


def create_ragflow_client(credentials: dict[str, Any]) -> Any:
    api_key = str(credentials.get("api_key"))
    base_url = str(credentials.get("base_url"))
    ragflow_module = importlib.import_module("ragflow_sdk")
    ragflow_class = getattr(ragflow_module, "RAGFlow")
    return ragflow_class(api_key=api_key, base_url=base_url)


def find_memory(client: Any, memory_id: str, page_size: int = 100) -> Any:
    page = 1
    while True:
        result = client.list_memory(page=page, page_size=page_size)
        memories = result.get("memory_list", [])
        for memory in memories:
            if getattr(memory, "id", None) == memory_id:
                return memory
        if len(memories) < page_size:
            break
        page += 1
    raise ValueError(f"Memory with ID {memory_id} not found")
