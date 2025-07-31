import zlib
import base64
from functools import wraps

# Only compress values under these keys:
TARGET_KEYS = {"address", "intArray", "stringArray", "bitCodes"}

def compress_array(value):
    if isinstance(value, (list, str, bytes)):
        raw = str(value).encode("utf-8")
        compressed = zlib.compress(raw)
        return base64.b64encode(compressed).decode("utf-8")
    return value  # Leave it untouched if it's not compressible

def deep_compress(data):
    if isinstance(data, dict):
        return {
            key: compress_array(value) if key in TARGET_KEYS else deep_compress(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [deep_compress(item) for item in data]
    else:
        return data  # Return value untouched

def compress_nested_arrays(func=None, *, verbose=False):
    def decorator(inner_func):
        @wraps(inner_func)
        def wrapper(*args, **kwargs):
            original = inner_func(*args, **kwargs)
            compressed = deep_compress(original)
            if verbose:
                print(f"[Compressed Result]: {compressed}")
            return compressed
        return wrapper

    if func is None:
        return decorator
    return decorator(func)

# ----------------

import zlib
import base64

# The same keys we compressed before
TARGET_KEYS = {"address", "intArray", "stringArray", "bitCodes"}

def decompress_array(value):
    if isinstance(value, str):
        try:
            compressed = base64.b64decode(value)
            raw = zlib.decompress(compressed)
            # The original was a stringified list or string, we eval to convert back
            return eval(raw.decode("utf-8"))
        except Exception:
            # If it's not decompressible, just return as is
            return value
    return value

def deep_decompress(data):
    if isinstance(data, dict):
        return {
            key: decompress_array(value) if key in TARGET_KEYS else deep_decompress(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [deep_decompress(item) for item in data]
    else:
        return data  # Base case: leave value unchanged


# -----

@compress_nested_arrays(verbose=True)
def get_data():
    return {
        "user": {
            "address": "123 Fake Street",
            "details": {
                "intArray": [1, 2, 3],
                "stringArray": ["hello", "world"],
                "notes": "Not compressing this",
            },
        },
        "bitCodes": [0, 1, 0, 1],
    }

compressed = get_data()
print("\n[Decompressed Result]:")
print(deep_decompress(compressed))



# ------

@overloader(intValue=1)
def get_data():
    return 1

@overloader(string="hello")
def get_data():
    return "gggg"


@overloader(strList=['a', 'b', 'c'])
def get_data():
    return ['a', 'b']


@overloader(intList=[1, 2, 3])
def get_data():
    return [1, 2, 3]


@overloader(objValue={})
def get_data():
    return {
        a: 'hello',
        b: 'world',
    }



compressed = get_data()
