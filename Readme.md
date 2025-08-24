# True Randomness with Random.org (Python Examples)

This repository demonstrates how to generate **true random numbers** using the [Random.org](https://www.random.org/clients/http/api/) services.  
Unlike pseudo-random generators (like Python's `random`), Random.org provides randomness derived from **atmospheric noise**.

We include **discrete examples** showing how to connect to different Random.org APIs and wrappers.

---

## Examples Included

### 1. HTTP GET API (No API key required)
- Uses the simple **HTTP GET** interface.
- Fetches random integers directly from: `https://www.random.org/integers/`
- Best for **quick testing** or one-off usage.
- Example:  
  ```python
  numbers = fetch_true_random_integers(5, 1, 100)
  print(numbers)  # [23, 77, 5, 91, 46]

### 2. JSON-RPC API (POST request)
Uses the more powerful JSON-RPC interface via https://api.random.org/json-rpc/4/invoke.

Requires an API key from Random.org.

Supports signed results and structured responses.

Example:

python
Copy
Edit
nums, sig = fetch_random_jsonrpc(api_key, 5, 0, 100, signed=True)
print(nums, sig)

### 3. Official rdoclient Wrapper
Demonstrates the official Random.org Python client.

Handles requests and optional caching automatically.

Supports signed integers and other generators.

Example:

python
Copy
Edit
nums, sig = fetch_with_rdoclient(api_key, 5, 0, 10, signed=True)
print(nums, sig)

### 4. py-random-dot-org Convenience Wrapper
Uses the py-random-dot-org package for a higher-level API.

Provides easy access to integers, strings, sequences, UUIDs, blobs, Gaussian numbers, and usage stats.

Example:

python
Copy
Edit
api = BasicApi(api_key=api_key)
print(api.generate_integers(num=5, minimum=1, maximum=100))
