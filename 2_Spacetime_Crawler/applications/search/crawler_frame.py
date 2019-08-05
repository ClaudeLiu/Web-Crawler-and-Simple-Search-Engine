import logging
from datamodel.search.TianzelZiyangc2Zijianx1_datamodel import TianzelZiyangc2Zijianx1Link, OneTianzelZiyangc2Zijianx1UnProcessedLink
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4
from bs4 import BeautifulSoup
import io

from urlparse import urlparse, parse_qs, urljoin
from uuid import uuid4

logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"

@Producer(TianzelZiyangc2Zijianx1Link)
@GetterSetter(OneTianzelZiyangc2Zijianx1UnProcessedLink)
class CrawlerFrame(IApplication):
    app_id = "TianzelZiyangc2Zijianx1"

    def __init__(self, frame):
        self.app_id = "TianzelZiyangc2Zijianx1"
        self.frame = frame


    def initialize(self):
        self.count = 0
        links = self.frame.get_new(OneTianzelZiyangc2Zijianx1UnProcessedLink)
        if len(links) > 0:
            print "Resuming from the previous state."
            self.download_links(links)
        else:
            l = TianzelZiyangc2Zijianx1Link("http://www.ics.uci.edu/")
            print l.full_url
            self.frame.add(l)

    def update(self):
        unprocessed_links = self.frame.get_new(OneTianzelZiyangc2Zijianx1UnProcessedLink)
        if unprocessed_links:
            self.download_links(unprocessed_links)

    def download_links(self, unprocessed_links):
        for link in unprocessed_links:
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            links = extract_next_links(downloaded)
            for l in links:
                if is_valid(l):
                    self.frame.add(TianzelZiyangc2Zijianx1Link(l))

    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")
    
def extract_next_links(rawDataObj):
    outputLinks = []
    '''
    rawDataObj is an object of type UrlResponse declared at L20-30
    datamodel/search/server_datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded. 
    The frontier takes care of that.
    
    Suggested library: lxml
    '''
    if rawDataObj.is_redirected == True:
        base_url = rawDataObj.final_url
        outputLinks.append(base_url)
    else:
        base_url = rawDataObj.url
        
    if rawDataObj.content == "":
        return outputLinks
    else:
        soup = BeautifulSoup(rawDataObj.content, "lxml")
        for link in soup.find_all('a'):
            url = urljoin(base_url, link.get('href'))
            outputLinks.append(url)

    parsed = urlparse(base_url)
    file_sub = open("/spacetime-crawler/applications/search/subdomain.txt", "a")
    if "ics.uci.edu" in str(parsed.netloc.encode("utf-8")):
        file_sub.write(str(parsed.netloc.encode("utf-8")) + '\n')
        print "netlock is: " + parsed.netloc


    number, invalid = Analysis(outputLinks)
    filer = io.open("/spacetime-crawler/applications/search/Valid_outlink.txt", mode="r", encoding="utf-8")
    rawDataObj.url = str(rawDataObj.url.encode("utf-8"))

    diction1 = {}  # Create dictionary to store information of the anlytics file
    diction2 = {}

    file1 = open("/spacetime-crawler/applications/search/Valid_outlink.txt", "a")
    file1.write(rawDataObj.url + " -> " + str(number) + '\n')

    file2 = open("/spacetime-crawler/applications/search/Invalid_outlink.txt", "a")
    file2.write(rawDataObj.url + " -> " + str(invalid) + '\n')

    return outputLinks

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    '''
    parsed = urlparse(url)
    url_encode = str(url.encode("utf-8"))
    slash_count = 0
    for i in url_encode:
        if i == "/":
            slash_count += 1
        if slash_count > 15:
            return False
    if parsed.scheme not in set(["http", "https"]):
        return False
    if parsed.netloc == '':   #double check whether the url is absolute url
        return False
    if parsed.fragment != '':   #check whether fragment section exists
        filew = open("/spacetime-crawler/applications/search/fragsec.txt", "a")
        filew.write(url_encode +"\n")
        filew.close()
        return False
    if parsed.geturl() == 'https://today.uci.edu/department/information_computer_sciences' or parsed.netloc == 'calendar.ics.uci.edu':
        return False
    if parsed.scheme == "mailto" or parsed.netloc == "ganglia.ics.uci.edu":
        return False
    if parsed.query != '':
        diction = {}
        filer = open("/spacetime-crawler/applications/search/dynamurl.txt", "r")
        for line in filer:
            url_count = line.rstrip('\n').split(' ')
            diction[url_count[0]] = int(url_count[1])
        temp_url = parsed.scheme + "://" + parsed.netloc + parsed.path
        if temp_url in diction:
            if diction[temp_url] > 50:
                return False
            else:
                diction[temp_url] += 1
        else:
            diction[temp_url] = 1
        filew = open("/spacetime-crawler/applications/search/dynamurl.txt", "w")
        for k,v in diction.items():
            filew.write(k+' '+str(v)+'\n')
        filer.close()
        filew.close()
    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False


def is_valid_url(url):
    '''
    This function is a duplicate function of is_valid() with same functionality
    But it stores the dynamic url and fragment in different text file to prevent
    from storing in the same file
    '''
    parsed = urlparse(url)
    url_encode = str(url.encode("utf-8"))
    slash_count = 0
    for i in url_encode:
        if i == "/":
            slash_count += 1
        if slash_count > 15:
            return False
    if parsed.scheme not in set(["http", "https"]):
        return False
    if parsed.netloc == '':  # double check whether the url is absolute url
        return False
    if parsed.fragment != '':  # check whether fragment section exists
        filew = open(
            "/spacetime-crawler/applications/search/fragsec111.txt",
            "a")
        filew.write(url_encode + "\n")
        filew.close()
        return False
    if parsed.geturl() == 'https://today.uci.edu/department/information_computer_sciences' or parsed.netloc == 'calendar.ics.uci.edu':
        return False
    if parsed.scheme == "mailto" or parsed.netloc == "ganglia.ics.uci.edu":
        return False
    if parsed.query != '':
        diction = {}
        filer = open(
            "/spacetime-crawler/applications/search/dynamurl111.txt",
            "r")
        for line in filer:
            url_count = line.rstrip('\n').split(' ')
            diction[url_count[0]] = int(url_count[1])
        temp_url = parsed.scheme + "://" + parsed.netloc + parsed.path
        if temp_url in diction:
            if diction[temp_url] > 50:
                return False
            else:
                diction[temp_url] += 1
        else:
            diction[temp_url] = 1
        filew = open(
            "/spacetime-crawler/applications/search/dynamurl111.txt",
            "w")
        for k, v in diction.items():
            filew.write(k + ' ' + str(v) + '\n')
        filer.close()
        filew.close()

    try:
        return ".ics.uci.edu" in parsed.hostname \
               and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                + "|thmx|mso|arff|rtf|jar|csv" \
                                + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        return False

def Analysis(ListUrl):
    '''
    Input is the outputLink, a list of urls inside one url
    @Return two ints which is the number of valid and invalid urls in the content of
    input url
    '''
    counter = 0
    invalid = 0
    for link in ListUrl:
        if is_valid_url(link): #Check if this link is valid
            counter +=1
        else:
            invalid +=1
    return counter, invalid
