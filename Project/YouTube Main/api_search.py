from YouTubeAPI import YouTubeAPI
import pandas as pd
from YT_SAVE_TO_DB import YT_SAVE_TO_DB
import pyodbc as odbc
from YT_NEW_VID_ID import YT_NEW_VID_ID
from YouTubeRelatedVideos import YouTube_Related_Videos
import re




# pattern = re.compile(r'watch\?v=')
# string = 'https://www.youtube.com/watch?v=qbexOeoH5hg'
# print(re.search(pattern,string))
# x = YT_NEW_VID_ID()
# print(x.get_next_related_video_id())
# x = ['',1,'1']
# print(x)
# x.remove('')
# print(x)
# conn = odbc.connect('Driver={SQL Server Native Client 11.0};'
#                                  'MultipleActiveResultSets={True};'
#                                  'Server=MAXIMUS2;'
#                                  'username = mabbas;'
#                                  'password = ninjaX3@;'
#                                  'Database=CRW_YT;'
#                                  'Trusted_Connection=yes;'
#                                  )
# cursor = conn.cursor()
# # sql_read = pd.read_csv('C:\\Users\\moham\\Desktop\\Python Projects\\YouTube\\Project\\SQL\\SQL_COMMANDS.csv')
# # sql = sql_read[sql_read['TABLE']=='YT_GET_NEXT_VID_IDS']['SQL'][4]
# # cursor.execute(sql)
# # result = cursor.fetchall()

y = YouTubeAPI(pd.read_json('api_key.json').loc()['api_key']['data'],'4-PjMoJx2bY')
z = YT_SAVE_TO_DB()
x = z.save_vid_details(z.get_video_details(),z.get_channel_details())
print(x)

