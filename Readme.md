# 🎲 True Randomness with Random.org (Python Examples)

This repository showcases how to generate **true random numbers** using [Random.org](https://www.random.org/clients/http/api/) — a service that delivers randomness derived from **atmospheric noise**, unlike traditional pseudo-random generators like Python’s `random`.

You'll find **clear, practical examples** demonstrating how to connect to various Random.org APIs and Python wrappers.

---

## 📦 What's Inside

### 1. 🌐 HTTP GET API (No API Key Required)
- Simple and direct interface using HTTP GET.
- Fetches random integers from: `https://www.random.org/integers/`
- Ideal for **quick tests** or one-off usage.

**Example:**
```python
numbers = fetch_true_random_integers(5, 1, 100)
print(numbers)  # [23, 77, 5, 91, 46]
```

---

### 2. 🔐 JSON-RPC API (POST Request)
- Uses the powerful JSON-RPC interface: `https://api.random.org/json-rpc/4/invoke`
- Requires an API key from Random.org.
- Supports **signed results** and structured responses.

**Example:**
```python
nums, sig = fetch_random_jsonrpc(api_key, 5, 0, 100, signed=True)
print(nums, sig)
```

---

### 3. 🧰 Official `rdoclient` Wrapper
- Demonstrates usage of the official Random.org Python client.
- Automatically handles requests and optional caching.
- Supports signed integers and other generators.

**Example:**
```python
nums, sig = fetch_with_rdoclient(api_key, 5, 0, 10, signed=True)
print(nums, sig)
```

---

### 4. 🛠️ `py-random-dot-org` Convenience Wrapper
- High-level API via the `py-random-dot-org` package.
- Easily generate integers, strings, sequences, UUIDs, blobs, Gaussian numbers, and usage stats.

**Example:**
```python
api = BasicApi(api_key=api_key)
print(api.generate_integers(num=5, minimum=1, maximum=100))
```

---

## 🚀 Getting Started
To run these examples, make sure you:
- Have Python 3 installed
- Install required packages via `pip`
- Obtain an API key from [Random.org](https://www.random.org/account/)
