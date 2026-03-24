from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, normalize_result, require_list


class RagflowGetRecentMessagesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        memory_id = require_list(tool_parameters.get("memory_id"), "memory_id")
        agent_id = tool_parameters.get("agent_id") or None
        session_id = tool_parameters.get("session_id") or None
        limit = tool_parameters.get("limit", 10)

        try:
            result = ragflow_client.get_recent_messages(
                memory_id=memory_id,
                agent_id=agent_id,
                session_id=session_id,
                limit=limit,
            )
            yield self.create_json_message(normalize_result(result))
        except Exception as e:
            raise ValueError(f"Get recent messages error: {e}")
