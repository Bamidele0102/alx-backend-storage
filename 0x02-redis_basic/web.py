#!/usr/bin/env python3
"""
A simple web scraper that caches the HTML content of a webpage using Redis.
"""
import requests
import redis
from functools import wraps
from datetime import timedelta


# Redis connection (consider environment variables for production)
redis_client = redis.Redis(host='localhost', port=6379)


def cache_with_expiry(expire_seconds: int = 10):
    """
    Decorator that caches function results with an expiration time.

    Args:
        expire_seconds: The expiration time for the cached result in seconds
        (default: 10).

    Returns:
        A decorator function.
    """

    def decorator(func):
        """
        Decorator function that caches the result of the
        decorated function"""
        @wraps(func)
        def wrapper(url):
            cache_key = f"count:{url}"
            cached_value = redis_client.get(cache_key)

            if cached_value:
                # Increment count from cache if already exists
                count = int(cached_value.decode()) + 1
                redis_client.set(cache_key, count, ex=expire_seconds)
                return cached_value.decode()

            # Fetch content if not cached
            content = func(url)
            redis_client.set(cache_key, content, ex=expire_seconds)
            redis_client.incr(cache_key)

            return content

        return wrapper

    return decorator


@cache_with_expiry(expire_seconds=10)  # Cache results for 10 seconds
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL using requests and returns it.

    Args:
        url: The URL of the webpage to retrieve.

    Returns:
        The HTML content of the webpage.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for non-2xx status codes
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/3000/url/wikipedia/en.html"

    # First request (no cache hit)
    content = get_page(url)
    print(content[:100])  # Print the beginning of the content

    # Second request (cache hit)
    content = get_page(url)
    print(content[:100])  # Content should be retrieved from cache
