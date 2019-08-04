
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 16:01:43 2018

@author: youngchen
"""
from __future__ import division
import json
import io
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import math
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import re
filePathNameWExt = './' + './' + '/' + 'index' + '.json'
filePathNameWExt1 = './' + './' + '/' + 'index1' + '.json'
info_list = set()

with io.open("/WEBPAGES_RAW/bookkeeping.json", 
             'r', encoding = 'utf-8') as bk:
    book = json.load(bk)
    

with io.open('/index1.json', 'r', encoding='utf-8') as fp:    
     indexer = json.load(fp)
with io.open('/index.json', 'r', encoding='utf-8') as fp:    
     no_normalize_indexer = json.load(fp)

def normal_dict():
    dict = {}
    counter = 0
    for key, value in indexer.items():
        counter += 1
        for k,v in value.items():
            if k in dict:
                dict[k] += v * v
            else:
                dict[k] = v * v
        dict[k] = math.sqrt(dict[k])
        print(k, ": ", dict[k], "--", counter)
    return dict


def normalize(dict):
    counter = 0
    for k,v in indexer.items():
        counter += 1
        for i in v:
            v[i] = round(v[i]/dict[i], 7)
        print(counter)
    with open(filePathNameWExt1, 'w') as fp:
        json.dump(indexer, fp)
    return


def find_docid(word):
    '''
    This function find docid which contains input word
    :return: a list of docid and its tfidf
    '''
    list_id = []
    if word in indexer.keys():
        tfidf = indexer[word]  # tfidf is a dict
        for k, v in sorted(tfidf.items(), key=lambda x: -x[1]):
            list_id.append( (k.encode('utf-8'), v))
    
    return list_id


def Retrieval(value):
    stopWords = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    while (True):
        keyword = raw_input("Please enter key term: ")
        words = re.findall(r"[a-zA-Z]+", keyword)
        words = [lemmatizer.lemmatize(i.lower().encode('utf-8')) for i in words if i.lower() not in stopWords]
        
        if keyword == "!":
            break
        else:
            print
            print "tokenized words list: ", words
            print("keyword: ", keyword)
            
        if len(words) == 0:
            print "invalid input"

        if len(words) == 1:
            display(words[0])
                
        else:
            if value == True:
                doc_list = set()
                scores = defaultdict(int)
    
                for word in words:
                    if word in indexer:
                        related_doc = indexer[word]
                    
                        term_tfidf = cal_term(word, related_doc)
                        for k,v in related_doc.items():
                            docid = k
                            tfidf = v
                            doc_list.add(docid)
                            scores[docid] += round(term_tfidf * tfidf, 2)
                    else:
                        continue
    
                counter = 1
                if len(scores) == 0:
                    print "no result found"
                else:
                    for doc, score in sorted(scores.items(), key = lambda x: x[1], reverse = True):
                        print counter, ' ', doc, ' ', book[doc]
                        print
                        if counter > 10:
                            break
                        counter += 1 
            else:
                no_cosine(words)
                

def display(term):
    result = find_docid(term)
    if result == []:
        print("no result found")
    else:
        for  i, doc in enumerate(result):
            print i+1,' ',doc[0],' ', book[doc[0]]
            print
            if i > 9:
                break
                

def cal_term(term, related_doc):
    '''
    It take a term and output its tf-idf
    '''
    len_of_doc = len(related_doc)
    idf = math.log10(37497/len_of_doc)
    tf = 1
    tfidf = tf * idf

    return tfidf

def no_cosine(words):
    '''
    @words is a list of input query
    display the highest ranking of result
    '''
    result = defaultdict(int)
    for word in words:
        related_doc = no_normalize_indexer[word]
        for docid, tfidf in related_doc.items():
            result[docid] += tfidf
    
    #result = sorted(result.items(), key = lambda x: -x[1])
    counter = 0
    for k,v in sorted(result.items(), key = lambda x: -x[1]):
        print book[k]
        print
        counter += 1
        if counter > 9:
            break
    
    
if __name__ == '__main__':
    # temp = normal_dict()
    # normalize(temp)
    Retrieval(True)
    print("finished!")
