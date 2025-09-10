import requests
from typing import Any

class PredictionServiceApiClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")

    def get_results(self, model_name: str | None = None, benchmark_name: str | None = None) -> dict[str, Any]:
        """
        Expected endpoint (optional): GET /results?model=...&benchmark=...
        Returns JSON serializable object that can be converted to DataFrame.
        """
        params = {}
        if model_name:
            params["model"] = model_name
        if benchmark_name:
            params["benchmark"] = benchmark_name

        resp = requests.get(f"{self.base}/results", params=params, timeout=6)
        resp.raise_for_status()
        return resp.json()
