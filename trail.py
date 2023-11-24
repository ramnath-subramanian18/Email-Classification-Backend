import pymongo

# Use 'localhost' as the hostname to connect to your MongoDB container
mongo_host = 'localhost'
mongo_port = 27017 
client = pymongo.MongoClient(mongo_host, mongo_port)

    # Check if the connection is successful
if client.server_info():
        print("Connected to MongoDB successfully!")

db = client['credentials']
collection = db['credentials']

# Now you can perform operations on the collection
# For example, to insert a document:
data = {'key12': 'value12'}
collection.insert_one(data)