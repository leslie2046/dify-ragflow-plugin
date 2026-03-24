from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, find_memory, require_string


class RagflowUpdateMessageStatusTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        memory_id = require_string(tool_parameters.get("memory_id"), "memory_id")
        message_id = tool_parameters.get("message_id")
        status = tool_parameters.get("status")

        try:
            memory = find_memory(ragflow_client, memory_id)
            memory.update_message_status(message_id=message_id, status=status)
            yield self.create_json_message(
                {"success": True, "memory_id": memory_id, "message_id": message_id, "status": status}
            )
        except Exception as e:
            raise ValueError(f"Update message status error: {e}")
