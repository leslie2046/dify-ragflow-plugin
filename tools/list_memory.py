from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, ensure_list, memory_to_json


class RagflowListMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        page = tool_parameters.get("page", 1)
        page_size = tool_parameters.get("page_size", 50)
        tenant_id = ensure_list(tool_parameters.get("tenant_id")) or None
        memory_type = ensure_list(tool_parameters.get("memory_type")) or None
        storage_type = tool_parameters.get("storage_type") or None
        keywords = tool_parameters.get("keywords") or None

        try:
            result = ragflow_client.list_memory(
                page=page,
                page_size=page_size,
                tenant_id=tenant_id,
                memory_type=memory_type,
                storage_type=storage_type,
                keywords=keywords,
            )
            payload = {
                "memory_list": [memory_to_json(memory) for memory in result.get("memory_list", [])],
                "total_count": result.get("total_count", 0),
            }
            yield self.create_json_message(payload)
        except Exception as e:
            raise ValueError(f"List memory error: {e}")
