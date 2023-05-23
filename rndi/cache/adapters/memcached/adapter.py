#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
import os
import time
from typing import Any, Optional

import jsonpickle
from rndi.cache.contracts import Cache


def provide_sqlite_cache_adapter(config: dict) -> Cache:
    return MemcachedCacheAdapter(
    )


class MemcachedCacheAdapter(Cache):

    def __init__(self, directory_path: str, ttl: int = 900, name: str = 'cache', options: Optional[dict] = None):
        pass

    def has(self, key: str) -> bool:
        return self.get(key) is not None

    def get(self, key: str, default: Any = None, ttl: Optional[int] = None) -> Any:
        pass

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> Any:
        pass

    def delete(self, key: str) -> None:
        pass

    def flush(self, expired_only: bool = False) -> None:
        pass
