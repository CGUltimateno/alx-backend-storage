#!/usr/bin/env python3
"""
a Python function that lists all documents in a collection
"""
import pymongo


def list_all(mongo_collection):
    """
    a Python function that lists all documents in a collection
    """
    return mongo_collection.find()
