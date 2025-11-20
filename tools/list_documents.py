from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ragflow_sdk import RAGFlow

class RagflowListDocumentsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        api_key = str(self.runtime.credentials.get("api_key"))
        base_url = str(self.runtime.credentials.get("base_url"))
        ragflow_client = RAGFlow(api_key=api_key, base_url=base_url)
        
        dataset_id = tool_parameters.get("dataset_id")
        page = tool_parameters.get("page", 1)
        page_size = tool_parameters.get("page_size", 30)
        keywords = tool_parameters.get("keywords", None)

        try:
            # Find dataset
            target_dataset = None
            # Iterate to find dataset. 
            datasets = ragflow_client.list_datasets(page=1, page_size=1000)
            for dataset in datasets:
                if dataset.id == dataset_id:
                    target_dataset = dataset
                    break
            
            if not target_dataset:
                raise ValueError(f"Dataset with ID {dataset_id} not found.")

            # List documents
            documents = target_dataset.list_documents(page=page, page_size=page_size, keywords=keywords)
            
            for document in documents:
                yield self.create_json_message(document.to_json())

        except Exception as e:
            raise ValueError(f"List documents error: {e}")
