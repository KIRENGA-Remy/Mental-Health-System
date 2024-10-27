# db_connection.py
import pymongo

url = 'mongodb://localhost:27017'
client = pymongo.MongoClient(url)
db = client['mental_health_system']
