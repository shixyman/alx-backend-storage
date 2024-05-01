#!/usr/bin/env python3
""" Redis Module """

import requests
import time
from functools import wraps

def cache(ttl=10):  # 10 seconds
    cache_data = {}

    def decorator(func):
        def wrapper(url):
            nonlocal cache_data
            now = time.time()
            if url in cache_data and now - cache_data[url][0] < ttl:
                return cache_data[url][1]
            result = func(url)
            cache_data[url] = (now, result)
            return result
        return wrapper
    return decorator

@cache()
def get_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def count_access(url: str):
    count_key = f"count:{url}"
    if count_key not in count_access.cache:
        count_access.cache[count_key] = 0
    count_access.cache[count_key] += 1

def get_page_with_count(url: str) -> str:
    count_access(url)
    return get_page(url)


# Example usage:
if __name__ == "__main__":
    """doc doc test"""
    url = 'http://slowwly.robertomurray.co.uk'
    content = get_page(url)
    print(content)  # This should print the fetched HTML content
