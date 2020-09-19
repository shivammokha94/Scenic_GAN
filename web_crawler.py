#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 23:05:56 2020

@author: smokha
"""


import urllib
import urllib.request
from bs4 import BeautifulSoup
import os
import uuid 


i=1
c = 0

def make_soup(url):
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    
    request =  urllib.request.Request(url,None,hdr)
    thepage = urllib.request.urlopen(request)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata

pg_start = 2
pg_end = 11

while pg_start<=pg_end:
    link = "https://www.gettyimages.com/photos/santorini-sunset?mediatype=photography&page=" +str(pg_start)+ "&phrase=santorini%20sunset&sort=mostpopular"
    
    print("At page number", pg_start)
    pg_start = pg_start + 1
    soup = make_soup(link)


    for img in soup.findAll('img'):
        temp = img.get('src')
        print(temp)
    
        if temp is None:
            continue
    
        elif temp[:1] == "/":
            image = link + temp
        else:
            image = temp
        
        print(image)    
        c = c+1
        
        save_path = '/Users/smokha/Projects/DCGAN/web_images'
    
        completeName = os.path.join(save_path, uuid.uuid4().hex[:6].upper())
                                
        image_file = open(completeName + ".jpeg", "wb")
        image_file.write(urllib.request.urlopen(image).read())
        image_file.close()


print("Total images:", c)