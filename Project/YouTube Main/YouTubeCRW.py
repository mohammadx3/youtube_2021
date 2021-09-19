import pandas as pd
import YouTubeAPI
import pyodbc as odbc
from YouTubeAPI import YouTubeAPI
from YT_SAVE_TO_DB import YT_SAVE_TO_DB
from YouTubeMain import YouTube_Related_Videos
from multiprocessing import Pool
from YT_NEW_VID_ID import YT_NEW_VID_ID
import gc

if __name__ == '__main__':

    try:
        y = str(input('Enter a video link for youtube: '))
        related_video_setup = YouTube_Related_Videos(y)
        x = YT_NEW_VID_ID()
        prev_vid_id = x.generate_next_vid_id()
        print(prev_vid_id)
        video_channel_info = YouTubeAPI(pd.read_json('api_key.json').loc()['api_key']['data'], prev_vid_id)

        while video_channel_info.is_Valid() == 'F':
            print('remove video id from database: ', prev_vid_id)
            x.YT_remove_videoid(prev_vid_id)
            x = YT_NEW_VID_ID()
            prev_vid_id = x.generate_next_vid_id()
            video_channel_info = YouTubeAPI(pd.read_json('api_key.json').loc()['api_key']['data'], prev_vid_id)

        save_channel_details = YT_SAVE_TO_DB(vid_details=video_channel_info.get_video_details(),
                                             channel_details=video_channel_info.get_channel_details())
        multiprocess_pool = Pool(processes=4)
        process2 = multiprocess_pool.apply_async(related_video_setup.run_final)
        print('before process start: ', video_channel_info.get_channel_details())
        process3 = multiprocess_pool.apply_async(save_channel_details.save_vid_details)
        multiprocess_pool.close()
        multiprocess_pool.join()
        scrap_data = process2.get()
        print(scrap_data)
        print(process3.get())
        single_pool = Pool()
        process4 = single_pool.apply_async(save_channel_details.save_to_DB,
                                           args=('https://www.youtube.com/watch?v=' + prev_vid_id, scrap_data))
        single_pool.close()
        single_pool.join()
        print(process4.get())
        while scrap_data is not None:
            del single_pool
            del related_video_setup
            del multiprocess_pool
            del video_channel_info
            del process4
            del process3
            del process2
            del x
            gc.collect()
            print('inside crawler loop')
            x = YT_NEW_VID_ID()
            current_vid_id = x.get_next_related_video_id()
            vid_data_to_save = x.generate_next_vid_id()
            print('for relational videos, page to scrap is: ', current_vid_id)
            print('Saving detailed video data for: ', vid_data_to_save)
            if prev_vid_id == current_vid_id:
                print(f'previous{prev_vid_id} and current video{current_vid_id} to scrap is the same')
                break
            prev_vid_id = current_vid_id
            video_channel_info = YouTubeAPI(pd.read_json('api_key.json').loc()['api_key']['data'], vid_data_to_save)
            save_channel_details = YT_SAVE_TO_DB(vid_details=video_channel_info.get_video_details(),
                                                 channel_details=video_channel_info.get_channel_details())
            while video_channel_info.is_Valid() == 'F':
                print('remove video id from database: ', prev_vid_id)
                x.YT_remove_videoid(prev_vid_id)
                x = YT_NEW_VID_ID()
                prev_vid_id = x.generate_next_vid_id()
                video_channel_info = YouTubeAPI(pd.read_json('api_key.json').loc()['api_key']['data'], prev_vid_id)


            multiprocess_pool = Pool()

            related_video_setup = YouTube_Related_Videos('https://www.youtube.com/watch?v=' + str(current_vid_id))
            process2 = multiprocess_pool.apply_async(related_video_setup.run_final)
            process3 = multiprocess_pool.apply_async(save_channel_details.save_vid_details)
            multiprocess_pool.close()
            multiprocess_pool.join()
            scrap_data = process2.get()
            print(process3.get())
            single_pool = Pool()
            process4 = single_pool.apply_async(save_channel_details.save_to_DB,
                                               args=('https://www.youtube.com/watch?v=' + current_vid_id, scrap_data))
            single_pool.close()
            single_pool.join()
            print(process4.get())
    except Exception as ex:
        print('Following Error while crawling: ', ex.with_traceback())
