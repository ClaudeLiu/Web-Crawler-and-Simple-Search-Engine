from __future__ import division
from bs4 import BeautifulSoup
from lxml import html
import json
import re
import io
import os
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math


filePathNameWExt = './' + './' + '/' + 'index' + '.json'
#open json and get to all the files
stopWords = set(stopwords.words('english'))


def create_indexer():
    dict = {}
    counter = 0
    unique_number = 0
    with open("/WEBPAGES_RAW/bookkeeping.json") as json_file:
        number_url = json.load(json_file)

    for key, value in number_url.items():
        counter += 1
        key = key.encode('utf-8')

        with open(("/WEBPAGES_RAW/" + key), 'r') as html_file:
            page = html_file.read()
        print(key + ":  " + str(counter))
        # print("Empty document: " + key + ":  " + str(counter))
            
        #get all the text from each html
        soup = BeautifulSoup(page, "lxml")
        text = soup.get_text()

        #tokenize, eliminate stop words and lemmatize
        tokens = re.findall(r"[a-zA-Z]+", text)
        lemmatizer = WordNetLemmatizer()
        filtered_sentence = [ lemmatizer.lemmatize(i.lower()).encode('utf-8') for i in tokens if not i.lower() in stopWords]
       
        for x in filtered_sentence:
            if x in dict:
                if key in dict[x]:
                    dict[x][key] += 1
                else:
                    dict[x][key] = 1
            else:
                dict[x] = {key: 1}

    dict = calculate_tfidf(dict, counter)

    #write into a json file called index.json
    with open(filePathNameWExt, 'w') as fp:
        json.dump(dict, fp)
    unique_number = len(dict)            
    return unique_number


def calculate_tfidf(diction, c):
    for k,v in diction.items():
        for k1, v1 in v.items():
            tf = 1 + math.log10(v1)
            idf = math.log10(c/len(v))
            diction[k][k1] = round(tf * idf, 2)
    return diction




if __name__ == '__main__':
    number = create_indexer()
    print("Unique number of token is: ",number)
    
    while(True):
        keyword = raw_input("Please enter key term: ")
        if keyword == "!":
            break
        else:
            print("keyword: ", keyword)
        with io.open(filePathNameWExt, 'r', encoding = 'utf-8') as fp:
            indexer = json.load(fp)
            for keys, values in indexer.items():
                counter = 0

                keys = keys.encode('utf-8')
                if keyword.lower() in keys:
                    for x in values[0]:
                        counter += 1
                        print counter
                        if counter >10:
                            break
                        x.encode('utf-8')
                        print ("/WEBPAGES_RAW/" + x)
    print("finished!")




