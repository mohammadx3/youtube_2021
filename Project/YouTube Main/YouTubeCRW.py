import logging

import pandas as pd
import YouTubeAPI
from YouTubeAPI import YouTubeAPI
from YT_SAVE_TO_DB import YT_SAVE_TO_DB
from YouTubeRelatedVideos import YouTube_Related_Videos
from multiprocessing import Pool
from YT_NEW_VID_ID import YT_NEW_VID_ID
import gc

def process_related_videos(video_link):
    related_video_setup = YouTube_Related_Videos(video_link)
    related_videos = related_video_setup.run_final()
    save_data = YT_SAVE_TO_DB()
    save_data.save_to_DB('https://www.youtube.com/watch?v='+related_video_setup.new_vid_id,related_videos)
    print('Related videos saved for :',related_video_setup.new_vid_id[32:44])

def process_save_vid_details(video_id):
    print('saving detail data for: ',video_id)
    if video_id == '':
        print('No detail to save')
        return 0
    vid_data = YouTubeAPI(pd.read_json('api_key.json').loc()['api_key']['data'],video_id)
    save_detail_data = YT_SAVE_TO_DB()
    save_info = save_detail_data.save_vid_details(vid_data.get_video_details(),vid_data.get_channel_details())
    print('saved details output:',save_info)
    print('Saved detailed video data for id: ',video_id)



if __name__ == '__main__':
    x = str(input('Enter a video link for youtube: '))
    process_related_videos(x)
    p_v = []
    try:
        while x is not None or x != '':
            print('loop begin')
            x = []
            v = []
            y = YT_NEW_VID_ID()
            z = y.get_new_vid_ids()

            for iter in y.get_next_related_video_id():
                if iter == x:
                    continue
                else:
                    next_related_video = iter
                    link = 'https://www.youtube.com/watch?v=' + next_related_video
                    x.append(link)
            for id in z:
                if id is not None or id != '':
                    v.append(id)
                else:
                    print('blank id removal.....')
                    y.YT_remove_videoid(id)

            print('list of videos(previous): ', p_v)
            if p_v == v and p_v != []:
                print('Api Quota has ended for the day, ending the process')
                break
            p_v = v
            print('list of videos(for related data): ', x)
            print('list of videos(for detailed data): ', v)
            all_process = Pool(processes=10)
            related_video_pool = all_process.map_async(process_related_videos,x)
            if v is not None or v != '':
                detail_video_pool = all_process.map_async(process_save_vid_details, v)

            all_process.close()
            all_process.join()
            x = y.get_next_related_video_id()[0]
            del related_video_pool
            del all_process
            del y
            del z
            gc.collect()
            print('loop completed: reinitiating............')
    except Exception as ex:
        print('Following Error while crawling: ', ex)
