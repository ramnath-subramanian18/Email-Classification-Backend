
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
from support_folder.list_label import list_label
def training_testing_model(email,password): 
    print('into label')
    data_frame = pd.read_csv('csv_file/output_file.csv')
    
    data_frame['subj'] = data_frame['subj'].str.replace(r'[0-9.,$€=?]', ' ', regex=True)
    column = data_frame['Label']
    labels=list_label(email,password)
    # data_frame = data_frame[data_frame['Label'].str.contains('|'.join(labels))]
    print('first')
    def remove_stopwords(sentence):
        # print('stop')
        if pd.isnull(sentence):
            return sentence
        with open('csv_file/stopwords.csv', 'r') as file:
            reader = csv.reader(file)
            stop_words = set(row[0] for row in reader)

        word_tokens = sentence.split()
        filtered_sentence = [word for word in word_tokens if word.lower() not in stop_words]
        return ' '.join(filtered_sentence)

    data_frame['subj'] = data_frame['subj'].apply(lambda x: remove_stopwords(x))
    data_frame = data_frame.applymap(lambda x: x.lower() if isinstance(x, str) else x)


    # stemmer = PorterStemmer()
    # def stem_words(sentence):
    #     # print('stem')
    #     if pd.isnull(sentence) or not isinstance(sentence, str):
    #         return sentence
    #     words = sentence.split()
    #     stemmed_words = [stemmer.stem(word) for word in words]
    #     return ' '.join(stemmed_words)
    print('before stemming')
    # data_frame['subj'] = data_frame['subj'].apply(stem_words)
    # Convert the columns to strings
    data_frame['subj'] = data_frame['subj'].astype(str)
    data_frame['from'] = data_frame['from'].astype(str)
    print('2')
    data_frame['subj'].fillna('', inplace=True)
    data_frame['from'].fillna('', inplace=True)
    data_frame['Label'].fillna('', inplace=True)
    tfidf_vectorizer = TfidfVectorizer()
    print('3')
    # print('vector')

    X_subj = tfidf_vectorizer.fit_transform(data_frame['subj'])
    X_from = tfidf_vectorizer.transform(data_frame['from'])
    print('4')

    X_combined = hstack((X_subj, X_from))
    y=data_frame['Label']
    print('5')
    
    X_train, X_test = X_combined[:-1], X_combined[-1:]
    y_train, y_test = y[:-1], y[-1:]
    print('6')
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print('7')
    # print(y_pred[0])
    y_pred[0] = re.sub(r'[^\w\s]', '', y_pred[0])
    y_pred[0] = y_pred[0].capitalize()
    y_pred[0] = y_pred[0].replace(" ", "")
    # print(y_pred)
    return y_pred[0]