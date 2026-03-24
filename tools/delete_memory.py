from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, require_string


class RagflowDeleteMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        memory_id = require_string(tool_parameters.get("memory_id"), "memory_id")

        try:
            ragflow_client.delete_memory(memory_id)
            yield self.create_json_message({"success": True, "memory_id": memory_id})
        except Exception as e:
            raise ValueError(f"Delete memory error: {e}")
