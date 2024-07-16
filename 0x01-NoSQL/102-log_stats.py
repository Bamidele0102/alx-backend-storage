#!/usr/bin/env python3
""" Log stats - new version """
from pymongo import MongoClient


client = MongoClient()
db = client.logs
collection = db.nginx

def log_stats():
    """
    Provides some stats about Nginx logs stored in MongoDB:
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

    print("IPs:")
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in top_ips:
        print(f"{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
