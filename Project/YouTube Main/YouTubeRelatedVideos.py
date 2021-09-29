import pandas as pd
from bs4 import BeautifulSoup as bs
from requests_html import AsyncHTMLSession
import asyncio
import time as t
import pyodbc as odbc
import re
from YT_NEW_VID_ID import YT_NEW_VID_ID


class YouTube_Related_Videos:

    def __init__(self,url):
        self.new_vid_id = ''
        self.url = url
        pass

    def return_url(self):
        return self.url

    async def process1_get_related_videos(self,url):
        try:
            self.asession = AsyncHTMLSession()
            if self.url == '' or self.url is None or len(self.url) != 43:
                self.url = 'https://www.youtube.com/watch?v=mAa_YaJ_7zM'

            self.vid_info = dict()
            self.a = t.time()
            if len(self.url) != 43 or re.search(r'watch\?v=', self.url) is None:
                self.url = 'https://www.youtube.com/watch?v=mAa_YaJ_7zM'


            self.new_vid_id = self.url[32:44]
            self.r = await self.asession.get(self.url)
            task = asyncio.create_task(self.r.html.arender(sleep=1,scrolldown=10,keep_page=True))
            print('before wait')
            await task
            print('after wait')
            self.titles = self.r.html.find('#dismissible')
            await self.asession.close()
            self.r.close()

        except Exception as EEE:
            print('Not a valid video link, resuming video crawl from DB: ', EEE)
        try:
            for self.item in self.titles:
                self.data = bs(self.item.html, 'lxml')
                self.sub_data = self.data.find_all('div', class_='metadata style-scope ytd-compact-video-renderer')
                for self.main_data in self.sub_data:
                    self.vid_info[self.main_data.find('span', id='video-title').text.strip()] = self.main_data.find('a', rel='nofollow')[
                        'href']

            self.b = t.time()
            print(f'Time taken to get the related video id`s: {self.b - self.a}')
            return (self.vid_info)

        except:
            print('link not found')

    def run_final(self):
        try:
            print('first step: ',self.url)
            task1 = asyncio.run(self.process1_get_related_videos(str(self.url)))
            self.rel_vids = task1
            return self.rel_vids

        except Exception as e:
            print('Some error while fetching the data ',e)









