from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ragflow_sdk import RAGFlow

class RagflowListChunksTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        api_key = str(self.runtime.credentials.get("api_key"))
        base_url = str(self.runtime.credentials.get("base_url"))
        ragflow_client = RAGFlow(api_key=api_key, base_url=base_url)
        
        dataset_id = tool_parameters.get("dataset_id")
        document_id = tool_parameters.get("document_id")
        page = tool_parameters.get("page", 1)
        page_size = tool_parameters.get("page_size", 30)
        keywords = tool_parameters.get("keywords", None)

        try:
            # Find dataset
            # Note: This is inefficient if there are many datasets, but SDK doesn't seem to have get_dataset(id)
            # We assume we can iterate to find it.
            target_dataset = None
            # We might need to page through datasets if there are many
            # For now, let's fetch a reasonable amount or loop until found
            # Assuming list_datasets supports large page_size or we just check first page for now
            # Ideally we should loop.
            
            # Optimization: If the SDK allows getting dataset by ID directly, that would be better.
            # But based on available info, we list.
            
            # Let's try to list with a large page size first
            datasets = ragflow_client.list_datasets(page=1, page_size=1000) 
            for dataset in datasets:
                if dataset.id == dataset_id:
                    target_dataset = dataset
                    break
            
            if not target_dataset:
                # Try one more page if not found? Or just fail.
                raise ValueError(f"Dataset with ID {dataset_id} not found.")

            # Find document
            target_document = None
            documents = target_dataset.list_documents(page=1, page_size=1000)
            for document in documents:
                if document.id == document_id:
                    target_document = document
                    break
            
            if not target_document:
                raise ValueError(f"Document with ID {document_id} not found in dataset {dataset_id}.")

            # List chunks
            chunks = target_document.list_chunks(page=page, page_size=page_size, keywords=keywords)
            
            for chunk in chunks:
                yield self.create_json_message(chunk.to_json())

        except Exception as e:
            raise ValueError(f"List chunks error: {e}")
