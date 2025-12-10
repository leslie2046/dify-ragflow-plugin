from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ragflow_api import RagflowClient


class RagflowRetrieveTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:

        api_key = str(self.runtime.credentials.get("api_key"))
        base_url = str(self.runtime.credentials.get("base_url"))

        client = RagflowClient(api_key=api_key, base_url=base_url)
        question = tool_parameters.get("question", '')
        dataset_id = tool_parameters.get("dataset_ids", '')
        similarity_threshold = tool_parameters.get("similarity_threshold", 0.2)
        vector_similarity_weight = tool_parameters.get("vector_similarity_weight", 0.3)
        rerank_id = tool_parameters.get("rerank_id", None)
        top_k = tool_parameters.get("top_k", 5)
        keyword = tool_parameters.get("keyword", False)
        use_kg = tool_parameters.get("use_kg", False)
        dataset_ids = dataset_id.split(",") if dataset_id else None
        parsed_data = {
            "question": question,
            "dataset_ids": dataset_ids,
            "similarity_threshold": similarity_threshold,
            "vector_similarity_weight": vector_similarity_weight,
            "top_k": top_k,
            "page":1,
            "page_size":top_k,
            "rerank_id": rerank_id,
            "keyword": keyword,
            "use_kg": use_kg
            }
        res = client.post(route_method='/api/v1/retrieval', data_obj=parsed_data)
        json = res.json()
        if json.get("code") != 0:
            error_msg = json.get("message", "Unknown error")
            yield self.create_text_message(f"Retrieval error: {error_msg}")
            return
        try:
            chunks = json.get("data", {}).get("chunks", [])
            records = []
            for chunk in chunks:
                title = chunk.get("document_keyword", "")
                record = {
                    "metadata": {
                        "path": chunk.get("document_keyword", ""),
                        "description": ""
                    },
                    "score": chunk.get("similarity", 0.0),
                    "title": title,
                    "content": chunk.get("content_with_weight", "") or chunk.get("content", ""),
                }
                records.append(record)
            yield self.create_json_message({"result": records})

        except Exception as e:
            raise ValueError(f"Retrieval error: {e}")