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
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that will store the history of inputs and outputs for a method"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        self._redis.rpush(key + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(key + ":outputs", str(output))
        return output

    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function"""
    key = method.__qualname__
    redis = method.__self__._redis
    count = redis.get(key).decode('utf-8')
    inputs = redis.lrange(key + ":inputs", 0, -1)
    outputs = redis.lrange(key + ":outputs", 0, -1)

    print(f"{key} was called {count} times:")
    for i, (input, output) in enumerate(zip(inputs, outputs)):
        print(f"{key}(*{input.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    """Cache class that will implement a simple caching system"""

    def __init__(self):
        """Initialize the Cache object"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, int, float]) -> str:
        """Store the input data in Redis and return a unique key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @call_history
    def get(self, key: str) -> Union[str, int, float]:
        """Get the data stored in Redis for a given key"""
        if key is int:
            return self.get_int(self._redis.get(key))
        elif key is str:
            return self.get_str(self._redis.get(key))
        elif key is None:
            return self._redis.get(key)
        else:
            return key(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """Get the data stored in Redis for a given key as a string"""
        return key.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Get the data stored in Redis for a given key as an integer"""
        return int(key.decode("utf-8"))

