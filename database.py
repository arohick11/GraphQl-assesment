from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["auctionDB"]

users = db["users"]
items = db["items"]
bids = db["bids"]
transactions = db["transactions"]
categories = db["categories"]