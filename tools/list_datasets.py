from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ragflow_sdk import RAGFlow

class RagflowListDatasetsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:

        api_key = str(self.runtime.credentials.get("api_key"))
        base_url = str(self.runtime.credentials.get("base_url"))
        ragflow_client = RAGFlow(api_key=api_key, base_url=base_url)
        page = tool_parameters.get("page", 1)
        page_size = tool_parameters.get("page_size", 30)
        try:
            datasets = ragflow_client.list_datasets(page=page, page_size=page_size)
            for dataset in datasets:
                yield self.create_json_message(dataset.to_json())
        except Exception as e:
            raise ValueError(f"List datasets error: {e}")
