#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
"""
Memcache implementation of standard Cache interface
"""
import json
import socket
from typing import Any, Optional

import jsonpickle
from pymemcache.client.base import Client
from pymemcache.client.retrying import RetryingClient
from pymemcache.exceptions import (
    MemcacheClientError,
    MemcacheServerError,
    MemcacheUnexpectedCloseError,
    MemcacheUnknownCommandError,
    MemcacheUnknownError,
)
from rndi.cache.adapters.memcached.types import IPv4Host, IPv4Port, TTL
from rndi.cache.contracts import Cache


def provide_memcached_cache_adapter(config: dict) -> Cache:
    """
    Get Memcached adapter instance
    :param config:
    :return: MemcachedCacheAdapter instance
    """
    return MemcachedCacheAdapter(
        host=config.get('CACHE_MEMCACHED_HOST', 'localhost'),
        port=config.get('CACHE_MEMCACHED_PORT', 11211),
    )


class MemcachedCacheAdapter(Cache):
    """
    Memcache implementation of standard Cache interface
    """

    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: float = 0.05  # seconds
    CONNECT_TIMEOUT: float = 5.0  # seconds
    TIMEOUT: float = 5.0  # seconds
    ENCODING: str = 'utf-8'

    _client: RetryingClient = None
    _ttl: TTL = 3600  # seconds

    def __init__(self, host: IPv4Host, port: IPv4Port = 11211, ttl: TTL = 3600) -> None:
        self._ttl = ttl
        self._client = RetryingClient(
            Client(
                server=(host, port),
                connect_timeout=self.CONNECT_TIMEOUT,
                timeout=self.TIMEOUT,
                encoding=self.ENCODING,
                default_noreply=False,
            ),
            attempts=self.RETRY_ATTEMPTS,
            retry_delay=self.RETRY_DELAY,
            retry_for=[
                MemcacheUnexpectedCloseError, MemcacheUnknownError, MemcacheServerError,
                MemcacheUnknownCommandError, MemcacheClientError,
                socket.timeout, socket.error,
            ],
        )

    def has(self, key: str) -> bool:
        return self.get(key) is not None

    def get(self, key: str, default: Any = None, ttl: Optional[int] = None) -> Any:
        cache_val = self._client.get(key=key)

        try:
            data = jsonpickle.decode(cache_val)
        except (json.decoder.JSONDecodeError, TypeError):
            data = cache_val

        if data is not None and ttl is None:
            return data

        if data is not None and ttl is not None:
            return self.put(key, data, ttl)

        if default is not None and callable(default):
            value = default()
            if isinstance(value, tuple):
                value, ttl = value
            return self.put(key, value, ttl)

    def put(self, key: str, value: Any, ttl: Optional[TTL] = None) -> Any:
        serialized = jsonpickle.encode(value)
        expire_in = self._ttl if ttl is None else ttl
        return self._client.set(
            key=key, value=serialized, expire=expire_in,
        )

    def delete(self, key: str) -> None:
        self._client.delete(key=key)

    def flush(self, expired_only: bool = False) -> None:
        self._client.flush_all()
