#!/usr/bin/env python3
"""Defines a function that  provides some stats
   about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

client = MongoClient()
db = client.logs
collection = db.nginx

def log_stats():
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    num_logs = collection.count_documents({})
    print(f"{num_logs} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status_check = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

if __name__ == "__main__":
    log_stats()
