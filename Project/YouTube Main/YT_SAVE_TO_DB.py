import pyodbc as odbc
import pandas as pd
import re
import time as t
import logging as log

class YT_SAVE_TO_DB:
    def __init__(self):
        pass


    def save_vid_details(self,vid_details,channel_details):
        self.vid_details = vid_details
        self.channel_details = channel_details
        self.conn = odbc.connect('Driver={SQL Server Native Client 11.0};'
                                 'MultipleActiveResultSets={True};'
                                 'Server=MAXIMUS2;'
                                 'username = mabbas;'
                                 'password = pass@12345;'
                                 'Database=CRW_YT;'
                                 'Trusted_Connection=yes;'
                                 )
        self.cursor = self.conn.cursor()
        self.sql = pd.read_csv('C:\\Users\\moham\\Desktop\\Python Projects\\YouTube\\Project\\SQL\\SQL_COMMANDS.csv').loc[0]['SQL']
        self.values = [self.vid_details['videoId'],
                       self.vid_details['title'],
                       self.vid_details['categoryId'],
                       self.vid_details['categoryName'],
                       self.vid_details['channelId'],
                       self.vid_details['publishedAt'],
                       self.vid_details['description'],
                       '',
                       self.vid_details['tags'],
                       self.vid_details['duration'],
                       self.vid_details['viewCount'],
                       self.vid_details['likeCount'],
                       self.vid_details['dislikeCount'],
                       self.vid_details['commentCount'],
                       self.vid_details['favoriteCount'],
                       ]
        try:
            self.cursor.execute(self.sql,self.values)
            self.result = self.cursor.fetchone()
            self.conn.commit()
            print(self.result)
            # self.cursor.close()
            # self.conn.close()
        except Exception as Ex:
            log.basicConfig(filename='error_logger.log', encoding='utf-8', level=log.Logger)
            log.info('Video Detail Save output: ' + self.vid_details['videoId']+' and Error detail from db:', Ex)
            print('some error occurred while saving video data for id: '+self.vid_details['videoId']+' , Error:', Ex)

    # def save_channel_details(self):
    #     self.conn = odbc.connect('Driver={SQL Server Native Client 11.0};'
    #                              'MultipleActiveResultSets={True};'
    #                              'Server=MAXIMUS2;'
    #                              'username = mabbas;'
    #                              'password = ninjaX3@;'
    #                              'Database=CRW_YT;'
    #                              'Trusted_Connection=yes;'
    #                              )
    #     self.cursor = self.conn.cursor()
        self.df = pd.read_csv('C:\\Users\\moham\\Desktop\\Python Projects\\YouTube\\Project\\SQL\\SQL_COMMANDS.csv')
        self.sql2 = self.df[self.df['TABLE']=='YT_CHANNEL_DETAIL']['SQL'][1]
        self.values2 = [self.channel_details['channelId'],
                        self.channel_details['title'],
                        self.channel_details['description'],
                        self.channel_details.get('country','xx'),
                        self.channel_details['channelViewCount'],
                        0,
                        0,
                        self.channel_details['subscriberCount'],
                        self.channel_details['hiddenSubscriberCount'],
                        self.channel_details['videoCount'],
                        ','.join(i for i in self.channel_details.get('topicIds','')),
                        self.channel_details['privacyStatus'],
                        self.channel_details['isLinked'],
                        self.channel_details['madeForKids']
                       ]
        try:
            self.cursor.execute(self.sql2, self.values2)
            self.result = self.cursor.fetchone()
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            return self.result[0]
        except Exception as Ex:
            log.basicConfig(filename='error_logger.log', encoding='utf-8', level=log.Logger)
            log.info('Video Detail Save output: ' + self.vid_details['videoId'] + ' and Error detail from db:', Ex)
            print('some error occurred while saving channel data for id '+self.vid_details['videoId']+' , Error:', Ex)

    def save_to_DB(self, orig_url, vid_data):
        self.orig_url = orig_url
        self.vid_data = vid_data
        self.pattern = r'https://www.youtube.com/watch?v='
        self.sequence = self.orig_url
        if self.orig_url is None or re.search(self.pattern[:29], self.sequence[:29]) is None:
            orig_url = 'https://www.youtube.com/watch?v=4VfqVpTz4Q4'
        self.source_id = self.orig_url[len(orig_url) - 11:]
        self.df = pd.DataFrame(columns=['source_id', 'related_id', 'stamp_date'])
        try:
            self.conn = odbc.connect('Driver={SQL Server Native Client 11.0};'
                                     'MultipleActiveResultSets={True};'
                                'Server=MAXIMUS2;'
                                'username = mabbas;'
                                'password = pass@12345;'
                                'Database=CRW_YT;'
                                'Trusted_Connection=yes;'
                                )
            self.cursor = self.conn.cursor()

        except:
            print('Error connecting to the database, please try again')
        try:
            if self.vid_data is None:
                print('no value retrieved from the link')
                raise ValueError('Did not received any data from the link')
            self.index = 0
            for self.key, self.value in self.vid_data.items():
                self.time_stamp = (
                        str(t.gmtime().tm_year) + '-' + str(t.gmtime().tm_mon) + '-' + str(t.gmtime().tm_mday) + ' ' + str(
                    t.gmtime().tm_hour) + ':' + str(t.gmtime().tm_min) + ':' + str(t.gmtime().tm_sec))
                self.df.loc[self.index] = [self.source_id, self.value[len(self.value) - 11:], self.time_stamp]
                self.index += 1

                self.flag = 'N'
                self.sql = ' DECLARE @EXIST_FLAG char(1)' \
                      ' EXEC	[dbo].[GET_VIDEXIST]' \
                      ' @SOURCE_ID = ?,' \
                      ' @RELATED_ID = ?,' \
                      ' @EXIST_FLAG = @EXIST_FLAG OUTPUT;' \
                      ' SELECT @EXIST_FLAG'

                self.values = (self.source_id, self.value[len(self.value) - 11:])
                self.cursor.execute(self.sql, (self.source_id, self.value[len(self.value) - 11:]))
                self.flag = self.cursor.fetchone()
                print('flag value: ',self.flag[0])
                if self.flag[0] == 'Y':
                    print(f'Video combination already in the database: {self.values[0]} and {self.values[1]}')
                    continue
                else:
                    pass
                print(f'Inserting video id`s in the database: {self.values[0]} and {self.values[1]}')
                self.cursor.execute('INSERT INTO dbo.YT_RELATED_VIDS (source_vid_id,related_vid_id,time_stamp) values (?,?,?)',
                               (self.source_id, self.value[len(self.value) - 11:], self.time_stamp))

            self.conn.commit()
            self.conn.close()
            print('saved relational video ids: ',self.source_id)


        except Exception as Exx :
            print(f'Error Inserting Video id to the database ,please try again: ', Exx)







