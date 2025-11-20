
import urllib.parse
import requests
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

def auth(credentials):
    base_url = credentials.get("base_url")
    api_key = credentials.get("api_key")
    if not api_key or not base_url:
        raise ToolProviderCredentialValidationError("App Key and URL are required")
    try:
        assert RagflowClient(api_key, base_url).get_app_id is not None
    except Exception as e:
        raise ToolProviderCredentialValidationError(str(e))

class RagflowClient:
    """RagFlow接口的處理器"""

    def __init__(self, api_key: str = '', base_url: str = ''):
        self.base_url = base_url
        self.app_id = api_key

    @property
    def get_app_id(self):
        return self.app_id

    def get_header(self):
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.app_id,
        }

    def post(self, route_method, data_obj: dict = None, params: dict = None):
        if data_obj is None:
            data_obj = {}
        if params is None:
            params = {}
        url = self.base_url + route_method
        if params:
            url = url + "?" + urllib.parse.urlencode(params)
        return requests.post(
            url=url,
            headers=self.get_header(),
            json=data_obj,
            verify=False
        )

    def get(self, route_method, params: dict = None):
        if params is None:
            params = {}
        url = self.base_url + route_method
        # 如果params有值，則將params轉為url參數
        if params:
            url = url + "?" + urllib.parse.urlencode(params)
            
        return requests.get(
            url=url,
            headers=self.get_header(),
            verify=False
        )

