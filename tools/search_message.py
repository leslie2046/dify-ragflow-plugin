from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from memory_tools import create_ragflow_client, normalize_result, require_list, require_string


class RagflowSearchMessageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ragflow_client = create_ragflow_client(self.runtime.credentials)
        query = require_string(tool_parameters.get("query"), "query")
        memory_id = require_list(tool_parameters.get("memory_id"), "memory_id")
        agent_id = tool_parameters.get("agent_id") or None
        session_id = tool_parameters.get("session_id") or None
        similarity_threshold = tool_parameters.get("similarity_threshold", 0.2)
        keywords_similarity_weight = tool_parameters.get("keywords_similarity_weight", 0.7)
        top_n = tool_parameters.get("top_n", 10)

        try:
            result = ragflow_client.search_message(
                query=query,
                memory_id=memory_id,
                agent_id=agent_id,
                session_id=session_id,
                similarity_threshold=similarity_threshold,
                keywords_similarity_weight=keywords_similarity_weight,
                top_n=top_n,
            )
            yield self.create_json_message(normalize_result(result))
        except Exception as e:
            raise ValueError(f"Search message error: {e}")
