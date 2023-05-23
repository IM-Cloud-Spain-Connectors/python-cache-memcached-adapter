from __future__ import annotations

import os
from logging import LoggerAdapter
from typing import List, Optional
from unittest.mock import patch

import pytest
from rndi.cache.adapters.memcached.adapter import MemcachedCacheAdapter
from rndi.cache.contracts import Cache
from rndi.cache.provider import provide_cache


@pytest.fixture
def adapters(logger):
    def __adapters() -> List[Cache]:
        setups = [
            {
                'CACHE_DRIVER': 'memcached',
                'CACHE_MEMCACHED_HOST': os.getenv('CACHE_MEMCACHED_HOST', 'localhost'),
                'CACHE_MEMCACHED_PORT': os.getenv('CACHE_MEMCACHED_PORT', 11211),
            },
        ]

        extra = {
            'memcached': provide_test_memcached_cache_adapter,
        }
        adapters = [provide_cache(setup, logger(), extra) for setup in setups]
        return adapters

    return __adapters


@pytest.fixture()
def logger():
    def __logger() -> LoggerAdapter:
        with patch('logging.LoggerAdapter') as logger:
            return logger

    return __logger


@pytest.fixture
def counter():
    class Counter:
        instance: Optional[Counter] = None

        def __init__(self):
            self.count = 0

        @classmethod
        def make(cls, reset: bool = False) -> Counter:
            if not isinstance(cls.instance, Counter) or reset:
                cls.instance = Counter()
            return cls.instance

        def increase(self, step: int = 1) -> Counter:
            self.count = self.count + step
            return self

    def __(reset: bool = False) -> Counter:
        return Counter.make(reset)

    return __


def provide_test_memcached_cache_adapter(config: dict) -> Cache:
    return MemcachedCacheAdapter(
        host=config.get('CACHE_MEMCACHED_HOST', 'localhost'),
        port=config.get('CACHE_MEMCACHED_PORT', 11211),
    )
