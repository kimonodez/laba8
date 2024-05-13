from datetime import datetime
import requests
import pandas as pd

class BaseDataLoader:

    def __init__(self, endpoint=None):
        self._base_url = endpoint

    def _validate_url(self, url):
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError("Invalid URL format. Must start with http:// or https://")

    def _get_req(self, resource, params=None, method="GET", timeout=10):
        if not self._base_url:
            raise ValueError("Base URL is not set. Please set a valid base URL.")
        req_url = self._base_url + resource
        if params is not None:
            if not isinstance(params, dict):
                raise ValueError("Params must be a dictionary.")
            response = requests.request(method, req_url, params=params, timeout=timeout)
        else:
            response = requests.request(method, req_url, timeout=timeout)
        if response.status_code != 200:
            msg = f"Unable to request data from {req_url}, status: {response.status_code}"
            if response.text and response.text.message:
                msg += f", message: {response.text.message}"
            raise RuntimeError(msg)
        return response.text

if __name__ == "__main__":
    loader = BaseDataLoader()
