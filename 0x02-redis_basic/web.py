import requests
import redis
import time
from functools import wraps

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def track_url_count(url):
    """
    Decorator function to track the count of a URL using Redis.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count_key = f"count:{url}"
            redis_client.incr(count_key)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def cache_result(expiration_time):
    """
    Decorator function to cache the result of a function using Redis.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"cache:{func.__name__}:{args}"
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')
            else:
                result = func(*args, **kwargs)
                redis_client.setex(cache_key, expiration_time, result)
                return result
        return wrapper
    return decorator

@track_url_count("http://slowwly.robertomurray.co.uk")
@cache_result(expiration_time=10)
def get_page(url):
    response = requests.get(url)
    return response.text

# Test the get_page function
url = "http://slowwly.robertomurray.co.uk"
print(get_page(url))  # This will be slow for the first time
print(get_page(url))  # This will be cached and return the result immediately

# Check the count of the URL
count_key = f"count:{url}"
print(f"URL accessed {redis_client.get(count_key).decode('utf-8')} times.")