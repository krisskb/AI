# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re
import csv
import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score

def buildCSV(imdbpath,test):
    if test:
        csvfile=open('./imdb_te.csv','w')
    else:
        csvfile=open('./imdb_tr.csv','w')
    columns=['text','polarity']
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    rowdict={}
    for pol in ['pos','neg']:
        polarity=0 if pol=='neg' else 1
        posdir=os.path.join(imdbpath,pol)
        files=os.listdir(posdir)
        for file in files:
            with open(os.path.join(posdir,file),'r') as f:
                rowdict['text']=f.read()
            #rowdict['row_number']=cnt
            rowdict['polarity']=polarity
            writer.writerow(rowdict)
    csvfile.close()

def clean_text(text):
    # remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # remove the characters [\], ['] and ["]
    text = re.sub(r"\\", "", text)    
    text = re.sub(r"\'", "", text)    
    text = re.sub(r"\"", "", text)    
    
    # convert text to lowercase
    text = text.strip().lower()
    
    # replace punctuation characters with spaces
    filters='!"\'#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
    translate_dict = dict((c, " ") for c in filters)
    translate_map = str.maketrans(translate_dict)
    text = text.translate(translate_map)

    return text

def senti_classifier(data,ngram,tfidf,stopwords,test_data):
    if tfidf:
        vectorizer = TfidfVectorizer(stop_words=stopwords,
                             preprocessor=clean_text,
                             ngram_range=(1,ngram))
    else:
        vectorizer = CountVectorizer(stop_words=stopwords,
                             preprocessor=clean_text,
                             ngram_range=(1,ngram))
    features=vectorizer.fit_transform(data['text'])
    test_features=vectorizer.transform(test_data['text'])
    model=SGDClassifier(loss='hinge',penalty='l1')
    model.fit(features,data['polarity'])
    return model.predict(test_features)

if __name__ == "__main__":
    imdbpath=r'/home/krish/Downloads/aclImdb/train'
    buildCSV(imdbpath,False)
    train_data=pd.read_csv('./imdb_tr.csv')
    train_data.sample(frac=1)
    stopwords=[]
    with open(os.path.join(imdbpath,'stopwords.en.txt'),'r') as f:
        stopwords=[line.rstrip() for line in f.readlines()]
    imdbpath=r'/home/krish/Downloads/aclImdb/test'
    buildCSV(imdbpath,True)
    test_data=pd.read_csv('./imdb_te.csv')
    test_data.sample(frac=1)
    tfidf=False
    ngram=1
    #print(test_data.shape)
    #print(train_data.shape)
    output=senti_classifier(train_data,ngram,tfidf,stopwords,test_data)
    print(output)
    print(accuracy_score(test_data['polarity'],output))
    tfidf=True
    output=senti_classifier(train_data,ngram,tfidf,stopwords,test_data)
    print(accuracy_score(test_data['polarity'],output))
    ngram=2
    output=senti_classifier(train_data,ngram,tfidf,stopwords,test_data)
    print(accuracy_score(test_data['polarity'],output))
    tfidf=False
    output=senti_classifier(train_data,ngram,tfidf,stopwords,test_data)
    print(accuracy_score(test_data['polarity'],output))