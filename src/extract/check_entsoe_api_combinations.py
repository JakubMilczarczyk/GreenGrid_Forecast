import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

if __name__=="__main__":

    load_dotenv()
    API_KEY = os.getenv("ENTSOE_API_KEY")
    BASE_URL = "https://web-api.tp.entsoe.eu/api"
    DOMAIN = "10YDK-1--------W"     # Paste domain code for entso-e API
    TODAY = datetime.now().replace(hour=0, minute=0)
    YESTERDAY = TODAY - timedelta(days=1)

    DOC_TYPES = ["A65", "A71", "A75", "A68", "A33", "A69", "A44", "A11"]
    PROCESS_TYPES = ["A01", "A16", "A46", "A51"]

    def test_combination(doc, proc):
        params = {
            "securityToken": API_KEY,
            "documentType": doc,
            "processType": proc,
            "in_Domain": DOMAIN,
            "periodStart": YESTERDAY.strftime("%Y%m%d%H%M"),
            "periodEnd": TODAY.strftime("%Y%m%d%H%M"),
        }

        # Add out_Domain if type reminds it
        if doc in ["A65", "A75", "A11"]:
            params["out_Domain"] = DOMAIN

        try:
            r = requests.get(BASE_URL, params=params)
            if r.status_code == 200:
                print(f"[OK] {doc}:{proc}")
            else:
                print(f"[FAIL] {doc}:{proc} → {r.status_code}")
        except Exception as e:
            print(f"[ERROR] {doc}:{proc} → {e}")

    # Test all combinations
    for doc in DOC_TYPES:
        for proc in PROCESS_TYPES:
            test_combination(doc, proc)
