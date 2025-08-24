"""

Using the JSON-RPC API (POST interface)—more powerful and structured

This method requires an API key and supports signed responses, quotas, and a richer protocol 
GitHub RANDOM.ORG

Direct use via HTTP POST

"""


import requests
import json

def fetch_random_jsonrpc(api_key, num, minimum, maximum, signed=False):
    """
    Uses JSON-RPC API to get random integers.
    If signed=True, returns signed response.
    """
    method = "generateSignedIntegers" if signed else "generateIntegers"
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "apiKey": api_key,
            "n": num,
            "min": minimum,
            "max": maximum,
            "replacement": True
        },
        "id": 1
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post("https://api.random.org/json-rpc/4/invoke", json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"random.org error: {data['error']}")
    result = data.get("result") or data.get("random")
    integers = result["data"]
    signature = data.get("signature") if signed else None
    return integers, signature

# Example usage:
if __name__ == "__main__":
    api_key = "YOUR_API_KEY_HERE"
    nums, sig = fetch_random_jsonrpc(api_key, 5, 0, 100, signed=False)
    print("Random:", nums, "Signature:", sig)
