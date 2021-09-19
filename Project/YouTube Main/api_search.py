from YouTubeAPI import YouTubeAPI
import pandas as pd




y = YouTubeAPI(pd.read_json('api_key.json').loc()['api_key']['data'],'DBXZWB_dNsw')
print(y.get_video_details())
