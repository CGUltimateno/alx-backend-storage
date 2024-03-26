#!/usr/bin/env python3
"""
a Python function that provides some
 stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def log_stats(mongo_collection, q_key=None, q_val=None):
    """
    a Python function that provides some
    stats about Nginx logs stored in MongoDB
    """
    return mongo_collection.count_documents({} if q_key is None and q_val is None else {q_key: q_val})


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    logs = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print(log_stats(logs))
    for method in methods:
        print("\tmethod {}: {}".format(method, log_stats(logs, "method", method)))


