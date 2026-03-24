from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, find_memory, normalize_result, require_string


class RagflowGetMessageContentTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        memory_id = require_string(tool_parameters.get("memory_id"), "memory_id")
        message_id = tool_parameters.get("message_id")

        try:
            memory = find_memory(ragflow_client, memory_id)
            result = memory.get_message_content(message_id)
            yield self.create_json_message(normalize_result(result))
        except Exception as e:
            raise ValueError(f"Get message content error: {e}")
