#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 22:56:21 2018

@author: youngchen
"""
from collections import defaultdict
import re

def Subdomain(path):
    counter = 0
    diction = defaultdict(int)
    for line in open(path):
        line = line.rstrip('\n').split(' -> ') #split the line
        #print line[1]
        #diction[line[0]] += 1   #Count the number of urls processed by that url
        counter += int(line[1])
    print counter
    return diction

diction1 = Subdomain("/Users/youngchen/Documents/Study/CS121/Assignment3/spacetime-crawler-master/Subdomain.txt")

file1 = open("/Users/youngchen/Documents/Study/CS121/Assignment3/spacetime-crawler-master/Subdomain.txt","w") #Open a file to store subdomain infor
print diction1
for k,v in sorted(diction1.items(), key = lambda x: -x[1]):
    file1.write(k +" -> " + str(v) + '\n')
file1.close()

def Number_of_outlinks(path):
    '''
    This function read the number of outlinks from Valid_outlink.txt
    and sort the number and write the url with most outlink back to Valid_outlink.txt
    '''
    diction = defaultdict(int)
    for line in open(path):
        line = line.rstrip('\n').split(' -> ')
        diction[line[0]] = int(line[1])
    return diction
        
diction = Number_of_outlinks("/Users/youngchen/Documents/Study/CS121/Assignment3/spacetime-crawler-master/Invalid_outlink.txt")

file2 = open("/Users/youngchen/Documents/Study/CS121/Assignment3/spacetime-crawler-master/Invalid_outlink.txt","w") #Open a file to store subdomain infor
for k,v in sorted(diction.items(),key = lambda x: -x[1]):
    print k,v
    file2.write(k +" -> " + str(v) + '\n')
file2.close()