import requests
import redis
import time
from functools import wraps

def cache_with_expiration(expires_in):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            redis_instance = redis.Redis()
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Check if the result is already cached
            cached_result = redis_instance.get(cache_key)
            if cached_result:
                print("Retrieving from cache...")
                return cached_result.decode("utf-8")

            # If not cached, fetch the page and cache the result
            response = requests.get(url)
            content = response.text
            redis_instance.set(cache_key, content, ex=expires_in)

            # Increment the access count for the URL
            redis_instance.incr(count_key)

            return content

        return wrapper

    return decorator

@cache_with_expiration(expires_in=10)
def get_page(url):
    response = requests.get(url)
    content = response.text
    return content