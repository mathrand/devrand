"""

Using the HTTP Integer Generator (simpler GET interface)

This API allows retrieving random integers via HTTP GET requests.

How it works

Endpoint: https://www.random.org/integers/

Parameters include num, min, max, col, base, format=plain, rnd=new (to ensure "true randomness") 
Random.org

Successful responses return plain-text numbers. Errors start with Error: 
Random.org

There are quotas based on bits—you should handle rate limits and quota exceptions 
Wikipedia Random.org

"""


import requests

def fetch_true_random_integers(num, minimum, maximum, base=10, cols=1):
    """
    Fetch 'num' true random integers between minimum and maximum (inclusive) from random.org via HTTP GET.
    Returns a list of integers.
    """
    url = "https://www.random.org/integers/"
    params = {
        "num": num,
        "min": minimum,
        "max": maximum,
        "col": cols,
        "base": base,
        "format": "plain",
        "rnd": "new"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    text = resp.text.strip()
    if text.startswith("Error:"):
        raise RuntimeError(f"random.org error: {text}")
    # parse numbers
    return [int(x, base) for x in text.split()]

# Example usage:
if __name__ == "__main__":
    try:
        numbers = fetch_true_random_integers(5, 1, 100)
        print("True random integers:", numbers)
    except Exception as e:
        print("Failed to fetch true random:", e)



