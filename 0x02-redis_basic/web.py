#!/usr/bin/env python3
""" Redis Module """

import requests
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def count_url_accesses(func):
    @wraps(func)
    def wrapper(url):
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(url)

    return wrapper


def cache_with_expiration(expiration):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            cache_key = f"cache:{url}"
            cached_content = redis_client.get(cache_key)
            if cached_content:
                return cached_content.decode('utf-8')
            else:
                response = func(url)
                redis_client.setex(cache_key, expiration, response)
                return response

        return wrapper

    return decorator


@count_url_accesses
@cache_with_expiration(expiration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text



# Example usage:
if __name__ == "__main__":
    """doc doc test"""
    url = 'http://slowwly.robertomurray.co.uk'
    content = get_page(url)
    print(content)  # This should print the fetched HTML content
