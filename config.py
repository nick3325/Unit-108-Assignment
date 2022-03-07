from http import client
import pymongo
import certifi


mongo_url = "mongodb+srv://NickFSDI:123@cluster0.dcaue.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_url, tlsCAFile=certifi.where())

#get specific DB
db = client.get_database("FitnessProducts")