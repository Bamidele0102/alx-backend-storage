#!/usr/bin/env python3
"""
lists all documents in a collection
"""
import pymongo


def list_all(mongo_collection):
    """
    Return a list of all documents in a collection or an empty list
    """
    return [] if not mongo_collection else list(mongo_collection.find())
