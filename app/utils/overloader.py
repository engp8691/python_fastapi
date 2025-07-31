from functools import wraps

# Registry to store all overloaded functions
_overload_registry = {}

def overloader(**signature):
    """
    Registers a function with a specific keyword signature.
    """
    def register_overload(func):  # Renamed from `decorator`
        key = tuple(sorted(signature.items()))  # make key hashable and consistent
        name = func.__name__

        # Store the function in the registry
        if name not in _overload_registry:
            _overload_registry[name] = {}

        _overload_registry[name][key] = func

        @wraps(func)
        def dispatcher(**kwargs):
            call_key = tuple(sorted(kwargs.items()))
            func_map = _overload_registry.get(name, {})
            matched = func_map.get(call_key)

            if not matched:
                raise ValueError(f"No overload of `{name}` matches arguments: {kwargs}")
            return matched(**kwargs)
        return dispatcher
    return register_overload

# Overloaded versions of `get_data`
@overloader(intValue=1)
def get_data(**kwargs):
    return 1

@overloader(string="hello")
def get_data(**kwargs):
    return "gggg"

@overloader(strList=['a', 'b', 'c'])
def get_data(**kwargs):
    return ['a', 'b']

@overloader(intList=[1, 2, 3])
def get_data(**kwargs):
    return [1, 2, 3]

@overloader(objValue={})
def get_data(**kwargs):
    return {
        "a": 'hello',
        "b": 'world',
    }

# Example usage
if __name__ == "__main__":
    print(get_data(intValue=1))           # ➜ 1
    print(get_data(string="hello"))       # ➜ "gggg"
    print(get_data(strList=['a', 'b', 'c']))  # ➜ ['a', 'b']
    print(get_data(intList=[1, 2, 3]))     # ➜ [1, 2, 3]
    print(get_data(objValue={}))          # ➜ {'a': 'hello', 'b': 'world'}

    # Uncomment to test an error case:
    # print(get_data(unknownKey=True))    # Raises ValueError
