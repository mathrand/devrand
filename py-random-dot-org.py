
"""
Convenience with py-random-dot-org wrapper

 If you prefer a higher-level package, py-random-dot-org
 offers easy methods for integers, sequences, strings, UUIDs, blobs, Gaussian numbers, and usage stats

"""

from py_random_dot_org.basic_api import BasicApi

def easy_random_example(api_key):
    api = BasicApi(api_key=api_key)
    print("Integers:", api.generate_integers(num=5, minimum=1, maximum=100))
    print("Usage stats:", api.get_usage())

if __name__ == "__main__":
    easy_random_example("YOUR_API_KEY_HERE")
