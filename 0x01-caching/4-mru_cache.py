#!/usr/bin/python3
"""The module for the MRUCache class"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    Inherits from BaseCaching and evicts Most recently referred block
    """

    def __init__(self):
        """Initialize"""
        super().__init__()

    def put(self, key, item):
        """Assign to the dictionary self.cache_data."""
        if key is None or item is None:
            return
        if key in self.cache_data:
            del self.cache_data[key]

        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            keyMost = list(self.cache_data.keys())[-1]
            self.cache_data.pop(keyMost)
            print('DISCARD: {}'.format(keyMost))
        self.cache_data[key] = item

    def get(self, key):
        """Must return the value in self.cache_data linked to key."""
        if key is None or key not in self.cache_data.keys():
            return None

        bit = self.cache_data.pop(key)
        self.cache_data[key] = bit
        return bit
