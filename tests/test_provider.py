#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
#
from rndi.cache.contracts import Cache
from rndi.cache.provider import provide_cache
from rndi.cache.adapters.memcached.adapter import (
    MemcachedCacheAdapter,
    provide_memcached_cache_adapter,
)


def test_make_cache_should_make_a_cache_adapter(logger):
    cache = provide_cache({'CACHE_DRIVER': 'memcached'}, logger(), {
        'memcached': provide_memcached_cache_adapter,
    })

    assert isinstance(cache, Cache)
    assert isinstance(cache, MemcachedCacheAdapter)
