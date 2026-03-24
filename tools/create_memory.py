from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, memory_to_json, require_list, require_string


class RagflowCreateMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        name = require_string(tool_parameters.get("name"), "name")
        memory_type = require_list(tool_parameters.get("memory_type"), "memory_type")
        embd_id = require_string(tool_parameters.get("embd_id"), "embd_id")
        llm_id = require_string(tool_parameters.get("llm_id"), "llm_id")

        try:
            memory = ragflow_client.create_memory(
                name=name,
                memory_type=memory_type,
                embd_id=embd_id,
                llm_id=llm_id,
            )
            yield self.create_json_message(memory_to_json(memory))
        except Exception as e:
            raise ValueError(f"Create memory error: {e}")
