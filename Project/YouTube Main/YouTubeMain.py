import os
import tkinter

import requests as req
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from selenium import webdriver as wdrv
from helium import *

# from webdriver-manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriver
# import pandas as pd
# from googleapiclient.discovery import build
# from Classes.HeaderandCookies import HeaderandCookie as HandC

import time


a = time.time()
url = 'https://www.youtube.com/watch?v=4VfqVpTz4Q4'
session = HTMLSession()
r = session.get(url)
r.html.render(sleep=1,keep_page=True,scrolldown=1)
# videos = r.html.xpath('//*[@id="video-title"]',first=True)
titles = r.html.find('#dismissible')
try:
    for item in titles:
        data = bs(item.html,'lxml')
        sub_data = data.find_all('div',class_='metadata style-scope ytd-compact-video-renderer')
        for main_data in sub_data:
            store = {'title':main_data.find('span',id='video-title').text.strip(),'link_code':main_data.find('a',rel='nofollow')['href']}
            print(store)
        # for title in titles:
        #     print(title.text.strip())
        # links = data.find_all('a',rel='nofollow')
        # for link in links:
        #     print(link['href'])
except:
    print('link not found')
b = time.time()
print(b - a)

#x = wdrv.Firefox(executable_path=r'C:\Users\moham\Desktop\Python Projects\YouTube\Imports\chromedriver.exe.exe',options=options)
#contents = data.find_all('div',class_='style-scope-ytd-item-section-renderer',id='contents')
# contents2 =content['aria-label']


# for content in contents:

# videos = r.html.xpath('//*[@id="video-title"]',first=True)

# for item in r.html.absolute_links:
#     x = session.get(item)
#     print(x.html.text)

# try:
#     for content in contents:
#         print(content)
# except:
#     pass



# data = resp.read()
# html = data.decode("UTF-8")
# print(html)
# api_key = os.environ.get("YT_API_KEY")
# api_key = pd.read_json("api_key.json").loc["api_key"]['data']
# service = build('youtube','v3',developerKey=api_key)
# request = service.channels().list(part='statistics',forUsername='schafer5')
