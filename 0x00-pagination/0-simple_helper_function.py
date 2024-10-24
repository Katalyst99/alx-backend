#!/usr/bin/env python3
"""The module for a simple helper function"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Function that takes two integer arguments and returns,
    a tuple of size two containing a start index and an end index
    """
    startIdx = (page - 1) * page_size
    endIdx = page * page_size
    return (startIdx, endIdx)
