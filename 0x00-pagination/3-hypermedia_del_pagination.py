#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """A method that returns a dictionary containing key-value pairs"""
        data = self.indexed_dataset()

        assert isinstance(index, int)
        assert isinstance(page_size, int) and page_size > 0
        assert 0 <= index < len(data)

        pageData = []
        currentIdx = index
        sizeNow = 0

        while sizeNow < page_size and currentIdx < len(data):
            if currentIdx in data:
                pageData.append(data[currentIdx])
                sizeNow += 1
            currentIdx += 1

        next_index = currentIdx

        return {
            "index": index,
            'data': pageData,
            'page_size': sizeNow,
            'next_index': next_index
        }
