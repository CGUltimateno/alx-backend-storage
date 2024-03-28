#!/usr/bin/env python3
"""
Define a Cache class that will implement a simple caching system
"""

import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that will count how many times a method is called"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that will store the history of inputs and outputs for a method"""

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function"""
        inputs = '{}:inputs'.format(method.__qualname__)
        outputs = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outputs, output)
        return output

    return wrapper


def replay(fn: Callable) -> None:
    """Display the history of calls of a particular function"""
    if fn is None or not hasattr(fn, '__name__'):
        return
    fn_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(fn_store, redis.Redis):
        return
    method_name = fn.__qualname__
    inputs = '{}:inputs'.format(method_name)
    outputs = '{}:outputs'.format(method_name)
    count = 0
    if fn_store.exists(inputs):
        count = int(fn_store.get(method_name))
        print('{} was called {} times:'.format(method_name, count))
        fn_inputs = fn_store.lrange(inputs, 0, -1)
        fn_outputs = fn_store.lrange(outputs, 0, -1)
        for fn_inputs, fn_outputs in zip(fn_inputs, fn_outputs):
            print('{}(*{}) -> {}'.format(method_name, fn_inputs.decode('utf-8'), fn_outputs.decode('utf-8')))


class Cache:
    """Cache class that will implement a simple caching system"""

    def __init__(self):
        """Initialize the Cache object"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis and return a unique key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """Get the data stored in Redis for a given key"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Get the data stored in Redis for a given key as a string"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Get the data stored in Redis for a given key as an integer"""
        return self.get(key, lambda x: int(x))
