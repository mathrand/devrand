"""

Using the official rdoclient wrapper (JSON-RPC Release 4 client)

The official Random.org Python client simplifies calls and supports caching

"""

from rdoclient import RandomOrgClient

def fetch_with_rdoclient(api_key, num, minimum, maximum, signed=False):
    """
    Fetch random integers using the official Random.org JSON-RPC client.
    """
    client = RandomOrgClient(api_key)
    if signed:
        result = client.generate_signed_integers(num, minimum, maximum)
        return result["data"], result.get("signature")
    else:
        data = client.generate_integers(num, minimum, maximum)
        return data, None

if __name__ == "__main__":
    client_key = "YOUR_API_KEY_HERE"
    nums, sig = fetch_with_rdoclient(client_key, 5, 0, 10, signed=True)
    print("Random:", nums, "Signature:", sig)
