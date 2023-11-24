import csv
import pandas as pd
import re
from collections import Counter
# from kafka import KafkaConsumer
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import csv
import pickle
#import openpyxl
import imaplib
import email
import re
import openai
from email.parser import BytesParser

def read_label_gpt(email,password,label1):
    # label1=["work","health and fitness:","education","family","ad","cab","jobs","shopping","trvael","ad"]
    api_key = "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"
    openai.api_key = api_key

    def classify_label(prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            stop=None,
            temperature=0,
        )
        return response["choices"][0]["text"].strip()


    # Define the file path
    file_path = "csv_file/output_file.csv"
    df = pd.read_csv(file_path)
    lst=[]
    dict1={}


    def write_to_csv(data):
        with open("csv_file/output_file.csv", mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write header row if needed
            # writer.writerow(['Column1', 'Column2', 'Column3', ...])

            # Write data rows
            for row in data:
                writer.writerow(row)

    def read():
        # all_mail=[]
        # df=pd.read_csv('csv_file/output_file.csv')
        # mail = imaplib.IMAP4_SSL('imap.gmail.com')
        # mail.login(email, password)
        # mail.select('INBOX')
        # status, data = mail.search(None, '(UNSEEN)')
        # status1, data1 = mail.uid('SEARCH', None, 'UNSEEN')
        # email_uids1= data1[0].split()
        # email_ids = data[0].split()
        # num_emails = min(2, len(email_ids))
        # for i in range(num_emails):
        #     email_uid1=email_uids1[i]
        #     email_id = email_ids[i]
        #     status1, data1 = mail.uid('FETCH', email_uid1, '(RFC822)')
        #     raw_email = data1[0][1]
        #     email_uid=email_uid1.decode()
        #     print(f"UID: {email_uid1.decode()}")
        #     status, data = mail.fetch(email_id, '(RFC822)')
        #     raw_email = data[0][1]

        #     email_message=BytesParser().parsebytes(raw_email)
        #     subject = email_message['Subject']
        #     from_address = email_message['From']

        #     # if isinstance(raw_email, str):
        #     #     raw_email = bytes(raw_email, 'utf-8')
        #     # print(raw_email)
        #     # email_message = email.message_from_bytes(raw_email)
        
            
        #     # subject = email_message['Subject']
        #     # from_address = email_message['From']
        #     print(subject)  
            
        #     prompt = f"Classify the following text into one of the categories: {label1}\n\n\"{subject}\""
            
        #     classified_label = classify_label(prompt)
        #     list_single_mail=[subject,from_address,classified_label]
        #     all_mail.append(list_single_mail)


        #     print("Classified Label:", classified_label)
            
        # mail.close()
        # mail.logout()
        # print(all_mail)
        all_mail=[['Nikhilesh, save up to 12%* on fares. Fly to Africa, Europe, the USA & more.', '=?UTF-8?B?UWF0YXIgQWlyd2F5cw==?= <email@qr.qatarairways.com>', 'Ad'], ['=?UTF-8?B?8J+RjQ==?= Your order was delivered', '"Walmart.com" <help@walmart.com>', 'Information']]
        write_to_csv(all_mail)


    for i in df['Label']:
        
        i1=re.sub(r'\s+|[^a-zA-Z0-9]', '', str(i))
        lst.append(i1.lower())

    dict1=(Counter(lst))
            
    lst_count=list(dict1.values())
    # print("count")
    # print((lst_count))
    
    
    i=0
    while(i<len(lst_count)):
        # print(i)
        if lst_count[i]<1:
            read()
            i=0
        else:
            i+=1
        # print(i)
    return 0
    