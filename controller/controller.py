from flask import Blueprint, request
from support_folder.label_classification import training_testing_model
from flask import Flask, request
from flask_cors import CORS, cross_origin
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import csv
from email.parser import BytesParser
import imaplib
import re
from model.mongodb import UserModel
from pymongo import MongoClient
from support_folder.read_mail import read_mail1
from support_folder.label_creation import label_creation
from read import read_label_gpt
from support_folder.label_classification import training_testing_model
from flask import Flask,request ,jsonify
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
import pymongo
import ssl
import hashlib
import jwt
import datetime
from functools import wraps
from model.mongodb import UserModel
from support_folder.list_label import list_label
from flask_cors import CORS
app=Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'your_secret_key_here'

form = Blueprint("form", __name__)
cors = CORS()
cors.init_app(form, resources={r"/*": {"origins": "*", "supports_credentials": True}})


# email=''
# password=''


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers.get('x-access-token')
        if not token:
            return 'token missing'
        data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
        print(data)
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
            data_key=data['public_id']
            client=pymongo.MongoClient('mongodb+srv://ramnath1:ramnath1@cluster0.agxnajm.mongodb.net/',ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
            db = client['user_account']
            collection = db['user_account']
            print(data_key)
            
            query = {
            "public_id": data_key
            }
            current_user = collection.find_one(query)
            print(current_user)
        except:
            return 'Token invalid'
        return f(current_user,*args,**kwargs)
    return decorated



@form.route("/form", methods=['POST'])
@token_required
def receive_data(current_user):
    
    user_model = UserModel() 
    req_Json=request.json
    print(req_Json)
    # user_model.insert_user(req_Json)
    if req_Json:
        global email,password
        email = req_Json['email']
        password=req_Json['password']
        print('email')
        # if user_model.check_user(req_Json['email']):

        #     email = req_Json['email']
        #     password=req_Json['password']
        #     # read_mail1(email,password)
        #     print('user exists')
        #     return 'user exists'
            
        # else:
        #     print('user doesnt exists')
        #     user_model.insert_user(req_Json)
        #     email = req_Json['email']
        #     password=req_Json['password']
        #     print(email,password)
    return 'Data Received'
    #user_model.insert_user(user_data)

@form.route("/label_form", methods=['POST'])
@token_required

def label_data(current_user):
    print("hello12")
    print("into label form")
    user_model = UserModel() 
    req_Json=request.json
    print(req_Json)
    print(email)
    matching_documents=(user_model.login(email))
    print('pasword printing')
    email_password=(matching_documents['email_password'])
    label_creation(email,email_password,req_Json)
    a=read_label_gpt(email,email_password,req_Json)
    read_mail1(email,email_password)
    # label=training_testing_model()
    # print((label))

    # new_values = {'subj': subject, 'from': from_address,'Label':label}
    # df = pd.read_csv('csv_file/output_file.csv')
    # df.iloc[-1] = new_values
    # df.to_csv(csv_file_path, index=False)
    # status, data = mail.uid('COPY', email_uid, label)

    # print(f"Subject: {subject}")
    # print(f"From: {from_address}")
        
        
    return 'Data Received'



@form.route('/register',methods=['POST'])
# @token_required
def create_user():
    print('into users')
    user_model = UserModel() 
    data=request.get_json()
    hashed_password=hashlib.sha512(data['password'].encode())
    print(hashed_password)
    if user_model.check_user(data['email']):
        print('user exists')
        # return ''
        return jsonify({'value': 'User_Exists'})  
    else:
        data = {
            'email': data['email'],
            'password': hashed_password.hexdigest(),
            'email_password':data['email_password'],
            'public_id':str(uuid.uuid4()),
            'admin':False
        }
        user_model.insert_user(data)
        return jsonify({'value': 'User_Created'})  
        # return 'User Created'

@form.route('/login',methods=['GET'])
# @token_required
def get_one_user():
    print('into login')
    user_model = UserModel() 
    global email,password
    email = request.args.get('email')
    password = request.args.get('password')

    hashed_password=hashlib.sha512(password.encode())
    hashed_pass_hexi=hashed_password.hexdigest()
    matching_documents=(user_model.login(email))
    print('matching documents')
    print(matching_documents)
    if(matching_documents==None):
        print('into this')
        return jsonify({'token':'password_invalid'})

    # print(matching_documents['password'])
    if(hashed_pass_hexi==matching_documents['password']):
        token=jwt.encode({'public_id':matching_documents['public_id'],'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        print(token)
        return jsonify({'token': token})    
    else:
        return jsonify({'token':'password_invalid'})

    
@form.route('/user',methods=['GET'])
@token_required
def get_all_users(current_user):
    user_model = UserModel() 
    all_documents=(user_model.find_all())
    for document in all_documents:
        print(document)
    return ''


@form.route('/trail',methods=['GET'])

def list_label1():
    print('into trail')
    return 'trail'    
    
