#!/usr/bin/env python3
"""
Define a Cache class that will implement a simple caching system
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that will count how many times a method is called"""
    @wraps(method)
    def wrapper(self, *data):
        """Wrapper function"""
        self._redis.rpush(f"{method.__qualname__}:inputs", str(data))
        uuid = method(self, *data)
        self.redis.rpush(f"{method.__qualname__}:outputs", uuid)
        return uuid
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that will store the history of inputs and outputs for a method"""
    @wraps(method)
    def wrapper(self, data):
        """Wrapper function"""
        self._redis.incr(method.__qualname__)
        output = method(self, data)
        return output
    return wrapper


def replay(method) -> None:
    """Display the history of calls of a particular function"""
    key = method.__qualname__
    _redis = redis.Redis()
    count = int(_redis.get(key).decode("utf-8"))
    print(f"{key} was called {count} times:")
    inputs = _redis.lrange(f"{key}:inputs", 0, -1)
    outputs = _redis.lrange(f"{key}:outputs", 0, -1)
    for i, (input, output) in zip(inputs, outputs):
        print(f"{key}(*{input.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    """Cache class that will implement a simple caching system"""

    def __init__(self):
        """Initialize the Cache object"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, float]) -> str:
        """Store the input data in Redis and return a unique key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """Get the data stored in Redis for a given key"""
        if fn is int:
            return self.get_int(self._redis.get(key))
        if (fn is str):
            return self.get_str(self._redis.get(key))
        if fn is None:
            return self._redis.get(key)
        else:
            return fn(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """Get the data stored in Redis for a given key as a string"""
        return key.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Get the data stored in Redis for a given key as an integer"""
        return int(key.decode("utf-8"))
