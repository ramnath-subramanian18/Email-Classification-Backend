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

def read_mail1(email,password):
    print("into read mail1")
    df=pd.read_csv('csv_file/output_file.csv')
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email, password)
    print("into read mail2")
    mail.select('INBOX')
    status, data = mail.search(None, '(UNSEEN)')
    status1, data1 = mail.uid('SEARCH', None, 'UNSEEN')
    email_uids1= data1[0].split()
    email_ids = data[0].split()
    num_emails =  len(email_ids)
    print(num_emails)
    for i in range(num_emails):
        email_uid1=email_uids1[i]
        email_id = email_ids[i]
        status1, data1 = mail.uid('FETCH', email_uid1, '(RFC822)')
        # raw_email = data1[0][1]
        email_uid=email_uid1.decode()
        print(f"UID: {email_uid1.decode()}")
        status, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        email_message=BytesParser().parsebytes(raw_email)
        subject = email_message['Subject']
        from_address = email_message['From']
        print(subject)
        new_row = {'subj': subject, 'from': from_address,'Label':'Information'}
        print(new_row)
        df = pd.concat([df, pd.DataFrame(new_row, index=[0])], ignore_index=True)
        csv_file_path = 'csv_file/output_file.csv'
        df.to_csv(csv_file_path, index=False)
        # print(df.head())
        label=training_testing_model(email,password)
        print((label))

        new_values = {'subj': subject, 'from': from_address,'Label':label}
        df = pd.read_csv('csv_file/output_file.csv')
        df.iloc[-1] = new_values
        df.to_csv(csv_file_path, index=False)
        status, data = mail.uid('COPY', email_uid, label)

        print(f"Subject: {subject}")
        print(f"From: {from_address}")
        
        if i == num_emails - 1:
            break 
        
    mail.close()
    mail.logout()
    
