#!/usr/bin/env python3
"""Defines a function that  provides some stats
   about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def log_stats():
    """Provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient()
    collection = client.logs.nginx

    doc_count = collection.count_documents({})
    print(f"{doc_count} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")
    status_check = collection.count_documents({"method": "GET",
                                                "path": "/status"})
    print(f"{status_check} status check")

if __name__ == "__main__":
    log_stats()
