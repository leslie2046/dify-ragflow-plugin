from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, find_memory, memory_to_json, parse_json_object, require_string


class RagflowUpdateMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        memory_id = require_string(tool_parameters.get("memory_id"), "memory_id")
        update_json = tool_parameters.get("update_json", "{}")

        try:
            memory = find_memory(ragflow_client, memory_id)
            updated_memory = memory.update(parse_json_object(update_json, "update_json"))
            yield self.create_json_message(memory_to_json(updated_memory))
        except Exception as e:
            raise ValueError(f"Update memory error: {e}")
