#!/usr/bin/env python
# coding: utf-8

import requests
import re
import json
import pandas as pd
import os
from modules.custom_exception import *
from random import randint
from bs4 import BeautifulSoup

def Check_Url(URL):    
    check = re.search(r"^https://www.timeanddate.com/weather/.*/historic$", URL)
    
    if not check:
        raise InvalidUrl()
        
    if os.path.exists(os.getcwd() + r'/resources/proxy.csv'):
        proxies = pd.read_csv(os.getcwd() + r'/resources/proxy.csv', encoding='utf-8').values.tolist()
    else:
        raise FileNotFound('proxy.csv')
        
    check_proxy = True
    
    while(check_proxy):
        if len(proxies) == 0:
            raise EmptyList('List proxy')
            
        rd_proxy = proxies[randint(0, len(proxies) - 1)]
            
        try:
            response = requests.get(URL, proxies={'https': rd_proxy[0]}, timeout=30)

            if response.status_code != 404 and not response.ok:
                proxies.remove(rd_proxy)
            else:
                check_proxy = False
                
        except Exception as err:
            proxies.remove(rd_proxy)
            
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
