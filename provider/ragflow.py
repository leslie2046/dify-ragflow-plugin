from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from ragflow_sdk import RAGFlow

class RagflowApiProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            api_key = str(credentials.get("api_key"))
            base_url = str(credentials.get("base_url"))
            ragflow_client = RAGFlow(api_key=api_key, base_url=base_url)
            ragflow_client.list_datasets()
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
