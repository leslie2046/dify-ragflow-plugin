from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, ensure_list, find_memory, normalize_result, require_string


class RagflowListMemoryMessagesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        memory_id = require_string(tool_parameters.get("memory_id"), "memory_id")
        agent_id = ensure_list(tool_parameters.get("agent_id")) or None
        keywords = tool_parameters.get("keywords") or None
        page = tool_parameters.get("page", 1)
        page_size = tool_parameters.get("page_size", 50)

        try:
            memory = find_memory(ragflow_client, memory_id)
            result = memory.list_memory_messages(
                agent_id=agent_id,
                keywords=keywords,
                page=page,
                page_size=page_size,
            )
            yield self.create_json_message(normalize_result(result))
        except Exception as e:
            raise ValueError(f"List memory messages error: {e}")
