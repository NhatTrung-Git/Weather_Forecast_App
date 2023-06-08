#!/usr/bin/env python
# coding: utf-8

import requests
import re
import pandas as pd
import os
from modules.custom_exception import *
from random import randint
from bs4 import BeautifulSoup

def Check_Url(URL):    
    check = re.search(r"^https://www.timeanddate.com/weather/.*/historic$", URL)
    
    if not check:
        raise InvalidUrl()
        
    response = requests.get(URL)
            
    if response.status_code == 404:
        raise FailedToFetch()
        
    soup = BeautifulSoup(response.content, 'html.parser')
    
    if 'Unknown address' in soup.find('h1', class_='headline-banner__title').text:
        raise FailedToFetch()
    
    
def ReadURL():
    if os.path.exists(os.getcwd() + r'/resources/url_data.csv'):
        urls = pd.read_csv(os.getcwd() + r'/resources/url_data.csv', encoding='utf-8', dtype={'End Date': str}).values.tolist()
    else:
        raise FileNotFound('url_data.csv')
        
    if os.path.exists(os.getcwd() + r'/resources/proxy.csv'):
        proxies = pd.read_csv(os.getcwd() + r'/resources/proxy.csv', encoding='utf-8').values.tolist()
    else:
        raise FileNotFound('proxy.csv')
    
    return urls, proxies
