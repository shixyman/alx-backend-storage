#!/usr/bin/env python3
import requests
import time
from functools import wraps
from typing import Dict, Callable

cache: Dict[str, str] = {}


def get_page(url: str) -> str:
    if url in cache:
        print(f"Retrieving from cache: {url}")
        return cache[url]
    else:
        print(f"Retrieving from web: {url}")
        response = requests.get(url)
        result = response.text
        cache[url] = result
        return result


def cache_with_expiration(expiration: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            key = f"count:{url}"
            if key in cache:
                count, timestamp = cache[key]
                if time.time() - timestamp > expiration:
                    result = func(*args, **kwargs)
                    cache[key] = (count + 1, time.time())
                    return result
                else:
                    cache[key] = (count + 1, timestamp)
                    return None
            else:
                result = func(*args, **kwargs)
                cache[key] = (1, time.time())
                return result

        return wrapper

    return decorator


@cache_with_expiration(expiration=10)
def get_page(url: str) -> str:
    if url in cache:
        print(f"Retrieving from cache: {url}")
        return cache[url]
    else:
        print(f"Retrieving from web: {url}")
        response = requests.get(url)
        result = response.text
        cache[url] = result
        return result
