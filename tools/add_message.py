from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, require_list, require_string


class RagflowAddMessageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        memory_id = require_list(tool_parameters.get("memory_id"), "memory_id")
        agent_id = require_string(tool_parameters.get("agent_id"), "agent_id")
        session_id = require_string(tool_parameters.get("session_id"), "session_id")
        user_input = require_string(tool_parameters.get("user_input"), "user_input")
        agent_response = require_string(tool_parameters.get("agent_response"), "agent_response")
        user_id = tool_parameters.get("user_id", "")

        try:
            message = ragflow_client.add_message(
                memory_id=memory_id,
                agent_id=agent_id,
                session_id=session_id,
                user_input=user_input,
                agent_response=agent_response,
                user_id=user_id,
            )
            yield self.create_json_message({"message": message})
        except Exception as e:
            raise ValueError(f"Add message error: {e}")
