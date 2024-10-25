"""Retrieval adapters"""
from .. import core


class WhooshIndex(core.AbstractIndex):
    def __init__(self):
        ...
        
    def search(self, query, num_results):
        ...
