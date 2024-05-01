import requests
import redis
import time

# Redis connection
redis_client = redis.Redis()


def track_url_count(url):
    # Increment the count for the given URL
    redis_client.incr(f"count:{url}")


def get_page(url):
    # Check if the URL is cached
    cached_page = redis_client.get(url)
    if cached_page:
        return cached_page.decode('utf-8')

    # Fetch the page content using requests
    response = requests.get(url)
    page_content = response.text

    # Cache the page content with an expiration time of 10 seconds
    redis_client.setex(url, 10, page_content)

    # Track the URL count
    track_url_count(url)

    return page_content
