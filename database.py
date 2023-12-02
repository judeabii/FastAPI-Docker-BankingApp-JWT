from pymongo import MongoClient

myclient = MongoClient("mongodb://mongo_db:27017")
db = myclient.bank
accounts_collection = db.accounts
user_collection = db.users
