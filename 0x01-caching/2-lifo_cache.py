#!/usr/bin/python3
"""The module for the LIFOCache class"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Inherits from BaseCaching and evicts the most recently added block"""

    def __init__(self):
        """Initialize"""
        super().__init__()

    def put(self, key, item):
        """Assign to the dictionary self.cache_data."""
        if key is None or item is None:
            return
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                keyL = list(self.cache_data.keys())[-1]
                self.cache_data.pop(keyL)
                print('DISCARD: {}'.format(keyL))
            self.cache_data[key] = item

    def get(self, key):
        """Must return the value in self.cache_data linked to key."""
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
