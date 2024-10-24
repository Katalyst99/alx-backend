#!/usr/bin/env python3
"""The module for hypermedia pagination"""
import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Function that takes two integer arguments and returns,
    a tuple of size two containing a start index and an end index
    """
    startIdx = (page - 1) * page_size
    endIdx = page * page_size
    return (startIdx, endIdx)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """A method that takes two integer arguments"""
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        startIdx, endIdx = index_range(page, page_size)
        data = self.dataset()

        if startIdx >= len(data):
            return []
        return data[startIdx:endIdx]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """A method that returns a dictionary containing key-value pairs"""
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        data = self.get_page(page, page_size)
        allData = len(self.dataset())
        total_pages = math.ceil(allData / page_size)
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": len(data),
            'page': page,
            'data': data,
            "next_page": next_page,
            "prev_page": prev_page,
            'total_pages': total_pages
        }
