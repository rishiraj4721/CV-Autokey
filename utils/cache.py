import json
import hashlib
import functools
import inspect
from pathlib import Path
from typing import Any, Callable, Optional, List


def json_cache(cache_file: str = "cache.json", key_args: Optional[List[str]] = None):
    """
    Decorator that caches function results in a JSON file.
    
    The cache key is: function_<SHA256_hash_of_specified_arguments>
    
    Args:
        cache_file: Path to the JSON cache file (default: "cache.json")
        key_args: List of argument names to use for cache key hashing.
                  If None, uses all non-self arguments.
                  
    Example:
        @json_cache(key_args=["url"])
        def extract_tech_keywords(self, url):
            return process(url)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create cache directory if it doesn't exist
            cache_path = Path(cache_file)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get function signature to map args to parameter names
            sig = inspect.signature(func)
            params = sig.parameters
            param_names = list(params.keys())
            
            # Build a dictionary of all arguments
            all_args = {}
            for i, arg in enumerate(args):
                if i < len(param_names):
                    all_args[param_names[i]] = arg
            all_args.update(kwargs)
            
            # Determine which arguments to use for cache key
            if key_args is None:
                # By default, exclude 'self' for methods
                cache_args = {k: v for k, v in all_args.items() if k != 'self'}
            else:
                # Use only specified arguments
                cache_args = {k: all_args.get(k) for k in key_args if k in all_args}
            
            # Convert to JSON string for hashing (only argument values, not names)
            cache_key_str = json.dumps(list(cache_args.values()), sort_keys=True, default=str)
            
            # Generate SHA256 hash of the input
            hashed_input = hashlib.sha256(cache_key_str.encode()).hexdigest()
            
            # Create cache key as function_hashedInput
            cache_key = f"{func.__name__}_{hashed_input}"
            
            # Load existing cache
            cache = {}
            if cache_path.exists():
                try:
                    with open(cache_path, "r") as f:
                        cache = json.load(f)
                except (json.JSONDecodeError, IOError):
                    cache = {}
            
            # Check if result is in cache
            if cache_key in cache:
                return cache[cache_key]
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            cache[cache_key] = result
            
            # Save cache to file
            try:
                with open(cache_path, "w") as f:
                    json.dump(cache, f, indent=2, default=str)
            except IOError as e:
                print(f"Warning: Could not write to cache file {cache_file}: {e}")
            
            return result
        
        return wrapper
    
    return decorator


# ==================== Example Usage ====================

# if __name__ == "__main__":
#     import time
    
#     # Example 1: Simple cache with default cache.json
#     @json_cache()
#     def add(a, b):
#         """Simple function that adds two numbers"""
#         print(f"Computing {a} + {b}...")
#         time.sleep(1)  # Simulate expensive operation
#         return a + b
    
#     # Example 2: Cache with custom file location
#     @json_cache()
#     def multiply(x, y):
#         """Multiply two numbers"""
#         print(f"Computing {x} * {y}...")
#         time.sleep(1)
#         return x * y
    
#     # Example 3: Cache with complex data types
#     @json_cache()
#     def process_list(items):
#         """Process a list of items"""
#         print(f"Processing {len(items)} items...")
#         time.sleep(1)
#         return {"count": len(items), "sum": sum(items), "avg": sum(items) / len(items)}
    
#     # Test the caching
#     print("--- Test 1: Basic caching ---")
#     print(f"First call: {add(5, 3)}")  # Executes function, waits 1s
#     print(f"Second call (cached): {add(5, 3)}")  # Returns immediately from cache
    
#     print("\n--- Test 2: Different inputs ---")
#     print(f"Different input: {add(10, 20)}")  # Different hash, executes again
    
#     print("\n--- Test 3: Custom cache file ---")
#     print(f"First call: {multiply(4, 6)}")  # Executes, saves to models_cache.json
#     print(f"Second call (cached): {multiply(4, 6)}")  # From cache
    
#     print("\n--- Test 4: Complex return types ---")
#     print(f"First call: {process_list([1, 2, 3, 4, 5])}")
#     print(f"Second call (cached): {process_list([1, 2, 3, 4, 5])}")
    
#     print("\n--- Cache files created ---")
#     print(f"cache.json exists: {Path('cache.json').exists()}")

