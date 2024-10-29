#!/usr/bin/python3
"""The module for the FIFOCache class"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    Inherits from BaseCaching and evicts blocks from cache,
    in their order of arrival.
    """

    def __init__(self):
        """Initialize"""
        super().__init__()

    def put(self, key, item):
        """Assign to the dictionary self.cache_data."""
        if key is None or item is None:
            return
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                keyF = list(self.cache_data.keys())
                self.cache_data.pop(keyF[0])
                print('DISCARD: {}'.format(keyF[0]))
            self.cache_data[key] = item

    def get(self, key):
        """Must return the value in self.cache_data linked to key."""
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
