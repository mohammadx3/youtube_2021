from googleapiclient.discovery import build
import pandas as pd
import re
import pyodbc as odbc

class YouTubeAPI:
    def __init__(self, api_key,video_id):
        if api_key == '' or api_key is None:
            print('Enter an api key before commencing')
        self.api_key = api_key
        self.video_id = video_id
        self.service = build('youtube', 'v3', developerKey=self.api_key)
        self.request = self.service.videos().list(part=['contentDetails', 'statistics', 'snippet','localizations','status','topicDetails'], id=[self.video_id])
        self.response = self.request.execute()
        self.valid = ''
        self.all_vid_details = dict()
        self.all_channel_details = dict()
        try:
            self.channelId = self.response['items'][0]['snippet']['channelId']
            self.request2 = self.service.channels().list(id=self.channelId,
                                                         part=['statistics', 'topicDetails', 'status', 'snippet',
                                                               'contentOwnerDetails', 'contentDetails'])
            self.response2 = self.request2.execute()
            self.request3 = self.service.videoCategories().list(part=['id','snippet'],id=self.response['items'][0]['snippet']['categoryId'])
            self.response3 = self.request3.execute()
            self.response3 = self.request3.execute()
            self.x = self.response['items'][0]['contentDetails']['duration']
            self.min_pattern = re.compile(r'(\d+)M')
            self.hour_pattern = re.compile(r'(\d+)H')
            self.secs_pattern = re.compile(r'(\d+)S')
            self.hours = int('0' if re.search(pattern=self.hour_pattern, string=self.x) is None else re.search(pattern=self.hour_pattern, string=self.x).group(1))
            self.mins = int('0' if re.search(pattern=self.min_pattern, string=self.x) is None else re.search(pattern=self.min_pattern, string=self.x).group(1))
            self.secs = int('0' if re.search(pattern=self.secs_pattern, string=self.x) is None else re.search(pattern=self.secs_pattern, string=self.x).group(1))
            self.__gen_video_details()
            self.__gen_channel_details()
        except Exception as E:
            print('API data could not be found: ', E)
            self.valid = 'F'




    def is_Valid(self):
        return self.valid

    def get_channelId(self):
        return self.channelId

    def get_video_response(self):
        return self.response

    def get_channel_response(self):
        return self.response2

    def __gen_video_details(self):
        try:
            self.all_vid_details['videoId'] = self.response['items'][0]['id']
            self.all_vid_details['categoryId'] = self.response['items'][0]['snippet']['categoryId']
            self.all_vid_details['tags'] = ','.join(str(i) for i in self.response['items'][0]['snippet'].get('tags',''))
            self.all_vid_details['description'] = self.response['items'][0]['snippet']['description']
            self.all_vid_details['categoryName'] = self.response3['items'][0]['snippet']['title']
            self.all_vid_details['commentCount'] = self.response['items'][0]['statistics'].get('commentCount','0')
            self.all_vid_details['viewCount'] = self.response['items'][0]['statistics']['viewCount']
            self.all_vid_details['likeCount'] = self.response['items'][0]['statistics'].get('likeCount',0)
            self.all_vid_details['dislikeCount'] = self.response['items'][0]['statistics'].get('dislikeCount',0)
            self.all_vid_details['favoriteCount'] = self.response['items'][0]['statistics']['favoriteCount']
            self.all_vid_details['duration'] = (self.hours*60*60) + (self.mins * 60) + self.secs
            self.all_vid_details['definition'] = self.response['items'][0]['contentDetails']['definition']
            self.all_vid_details['caption'] = self.response['items'][0]['contentDetails']['caption']
            self.all_vid_details['licensedContent'] = self.response['items'][0]['contentDetails']['licensedContent']
            self.all_vid_details['contentRating'] = self.response['items'][0]['contentDetails']['contentRating']
            self.all_vid_details['title'] = self.response['items'][0]['snippet'].get('title','')
            self.all_vid_details['publishedAt'] = self.response['items'][0]['snippet']['publishedAt'].replace('T',' ').replace('Z','')
            self.all_vid_details['channelId'] = self.response['items'][0]['snippet']['channelId']
        except Exception as E2:
            print('API video data could not be found: ',E2)
            self.valid = 'F'

    def get_video_details(self):
        return self.all_vid_details
    def __gen_channel_details(self):
        try:
            self.all_channel_details['channelId'] = self.response2['items'][0]['id']
            self.all_channel_details['title'] = self.response2['items'][0]['snippet']['title']
            self.all_channel_details['description'] = self.response2['items'][0]['snippet']['description']
            self.all_channel_details['publishedAt'] = self.response2['items'][0]['snippet']['publishedAt'].replace('T',' ').replace('Z','')
            self.all_channel_details['country'] = self.response2['items'][0]['snippet'].get('country','xx')
            self.all_channel_details['channelViewCount'] = self.response2['items'][0]['statistics']['viewCount']
            self.all_channel_details['subscriberCount'] = self.response2['items'][0]['statistics'].get('subscriberCount','')
            self.all_channel_details['hiddenSubscriberCount'] = self.response2['items'][0]['statistics']['hiddenSubscriberCount']
            self.all_channel_details['videoCount'] = self.response2['items'][0]['statistics']['videoCount']
            if self.response2['items'][0].get('topicDetails','') == '':
                self.all_channel_details['topicIds'] = ''
            else:
                self.response2['items'][0]['topicDetails'].get('topicIds','')
            self.all_channel_details['madeForKids'] = self.response2['items'][0]['status'].get('madeForKids','')
            self.all_channel_details['privacyStatus'] = self.response2['items'][0]['status'].get('privacyStatus','')
            self.all_channel_details['isLinked'] = self.response2['items'][0]['status'].get('isLinked','')
            self.all_channel_details['contentOwnerDetails'] = self.response2['items'][0].get('contentOwnerDetails','')
        except Exception as E:
            print('API channel data could not be found: ', E)
            self.valid = 'F'

    def get_channel_details(self):
        return self.all_channel_details

    def get_category_id(self):
        return self.response['items'][0]['snippet']['categoryId']

    def get_category_name(self):
        return self.response3['items'][0]['snippet']['title']

    def get_commentCount(self):
        return self.response['items'][0]['statistics']['commentCount']

    def get_duration_in_secs(self):
        return (self.hours*60*60) + (self.mins * 60) + self.secs










