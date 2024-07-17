#!/usr/bin/env python3
"""
A simple web scraper that caches the HTML content of a webpage using Redis.
"""
# web.py
import requests
import redis
from typing import Callable
import functools


# Initialize Redis client
redis_client = redis.Redis()


def count_access(method: Callable) -> Callable:
    """
    Decorator to count the number of accesses to a URL.
    """
    @functools.wraps(method)
    def wrapper(url: str, *args, **kwargs):
        """
        Wrapper function to count the number of accesses to a URL.
        """
        # Increment the count of accesses for the URL
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return method(url, *args, **kwargs)
    return wrapper


def cache_result(method: Callable) -> Callable:
    """
    Decorator to cache the result of a method using Redis.
    """
    @functools.wraps(method)
    def wrapper(url: str, *args, **kwargs):
        """
        Wrapper function to cache the result of a method using Redis.
        """
        # Define cache key and check if it exists
        cache_key = f"cache:{url}"
        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # Get the content and store it in cache
        content = method(url, *args, **kwargs)
        redis_client.setex(cache_key, 10, content)
        return content
    return wrapper


@count_access
@cache_result
def get_page(url: str) -> str:
    """
    Fetches the content of a webpage given its URL.
    """
    response = requests.get(url)
    return response.text


# Testing the function with simulated slow response
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/" \
               "http://www.example.com"

    print("First call (should fetch and cache):")
    print(get_page(test_url))

    print("\nSecond call (should use cache):")
    print(get_page(test_url))

    # Check the access count
    print("\nAccess count:")
    print(redis_client.get(f"count:{test_url}").decode('utf-8'))
