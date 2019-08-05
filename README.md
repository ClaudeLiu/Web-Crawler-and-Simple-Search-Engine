# Web Crawler and Simple Search Engine
**A crawler to extract as many links as possible given a base url and a search engine for users to retrieve relevant pages.** 

Techonologies and tools used:
1. [Python](https://www.python.org/)
2. [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
3. [Natural Language Toolkit(NLTK)](https://www.nltk.org/)

This project includes four parts.
<br><br>

## 1. Text Processing
The first program "./1_Text_Processing/PartA_wordFrequencies.py" 
takes a text file as a command line argument and outputs the word frequency in decreasing order.<br>
The second program "./1_Text_Processing/PartB_IntersectionOf2Files.py"
reads the contents of two text files and outputs the number of tokens they have in common.<br>

The purpose to write these two programs is that the crawler or the search engine may need text processing.

## 2. Spacetime Crawler
The most important file in this part is "./2_Spacetime_Crawler/applications/search/crawler_frame.py".<br>
The function "extract_next_links" extracts links from the content of a downloaded webpage.<br>
The function "is_valid_url" uses a bunch of rules to filter out crawler traps. This function returns True or False based on whether the url 
has to be downloaded or not.

## 3. Inverted Index
"./3_Inverted_Index/create_inverIndex.py" creates an inverted index for all the corpus (the webpages).<br>
nltk library is used to tokenize the text, filter the stop words and lemmatize the context to reduce the size of inverted index.<br>
TF-IDF and Cosine Similarity are applied to increase the quality and relevance of search result.

## 4. Search Engine
This is a simple search engine with command line interface. 
It takes search queries from users and presents a list of relevant urls to users in order.<br>
The ranking of search result follows a ranking formula. The formula includes TF-IDF and Cosine Similarity scoring.<br>
The search engine can handle any invalid search query.
  
