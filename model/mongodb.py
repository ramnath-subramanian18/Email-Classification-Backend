import pymongo
import ssl

class UserModel:
    def __init__(self):
        # self.client = pymongo.MongoClient('mongodb+srv://ramnath1:ramnath1@cluster0.agxnajm.mongodb.net/',ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
        # mongo_host = 'localhost'
        # mongo_port = 2717 
        # self.client = pymongo.MongoClient(mongo_host, mongo_port)
        # self.client = pymongo.MongoClient("mongodb://localhost:2717/")
        self.client = pymongo.MongoClient('mongodb+srv://ramnath1:ramnath1@cluster0.agxnajm.mongodb.net/')
        self.db = self.client['credentials']
        self.collection = self.db['credentials']

    def insert_user(self, user_data):
        # Insert the user data into the MongoDB collection
        print(user_data)
        self.collection.insert_one(user_data)

    def check_user(self, user_name):
        query = {'email': user_name}
        result = self.collection.find_one(query)
        if result:
            return 1  # User found
        else:
            return 0 
            
             # User not found
            
    def login(self, email):
        # print('into login')
        query = {'email': email}
        result = self.collection.find_one(query)
        # print(result)
        return result
    
    def find_all(self):
        all_documents = self.collection.find()
        return all_documents
    
        
    
