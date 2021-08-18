import os
import requests as req
from bs4 import BeautifulSoup as bs
from selenium import webdriver as wdrv

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriver
import pandas as pd
from googleapiclient.discovery import build
from Classes.HeaderandCookies import HeaderandCookie as HandC

import time

a = time.time()
url = 'https://www.youtube.com/watch?v=th5_9woFJmk'
# cookies = HandC().get_cookie()
# headers = HandC().get_header()
# session = HTMLSession()
# r = session.get(url)
# r.html.render(sleep=1,keep_page=True,scrolldown=1)
# data = r.html.find('#video-title')
# for video in data:
#     print(f'Title {video.text}')
#     print(f'Link {video.absolute_links}')



# page_data = req.get(url=url, cookies=cookies, headers=headers)
# page_content = bs(page_data.content,'html.parser')

option = wdrv.FirefoxOptions()
option.headless = True

x = wdrv.Firefox(executable_path=r'C:\Users\moham\Desktop\Python Projects\YouTube\Imports\geckodriver.exe',options=option)
x.get(url)
html = x.execute_script('return document.documentElement.outerHTML')
x.close()
data = bs(html, 'html.parser')
contents = data.find_all('a')
print(html)

# try:
#     for content in contents:
#         print(content)
# except:
#     pass

b = time.time()
print(b-a)





# data = resp.read()
# html = data.decode("UTF-8")
# print(html)
# api_key = os.environ.get("YT_API_KEY")
# api_key = pd.read_json("api_key.json").loc["api_key"]['data']
# service = build('youtube','v3',developerKey=api_key)
# request = service.channels().list(part='statistics',forUsername='schafer5')
