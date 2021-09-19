import pyodbc as odbc
import pandas as pd
import time as t
import re
class YT_NEW_VID_ID:
    def __init__(self):
        pass
    def generate_next_vid_id(self):
        df = pd.read_csv('C:\\Users\\moham\\Desktop\\Python Projects\\YouTube\\Project\\SQL\\SQL_COMMANDS.csv')
        self.sql = df[df['TABLE'] == 'GET_NEXT_VID_ID']['SQL'][2]
        try:
            self.conn = odbc.connect('Driver={SQL Server Native Client 11.0};'
                                     'MultipleActiveResultSets={True};'
                                     'Server=MAXIMUS2;'
                                     'username = mabbas;'
                                     'password = ninjaX3@;'
                                     'Database=CRW_YT;'
                                     'Trusted_Connection=yes;'
                                     )
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.sql)
            self.result_next_video = self.cursor.fetchone()
            self.new_vid_id = self.result_next_video[0]
            self.status = self.result_next_video[1]
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            if self.status == 'F':
                raise ValueError('No status was retrieved from database')
            return self.new_vid_id
        except Exception as er:
            print('Could not retrieve next video: ', er)

    def YT_remove_videoid(self,del_vid_id):
        self.del_vid_id = del_vid_id
        df = pd.read_csv('C:\\Users\\moham\\Desktop\\Python Projects\\YouTube\\Project\\SQL\\SQL_COMMANDS.csv')
        self.sql_del = df[df['TABLE'] == 'YT_REMOVE_INFO']['SQL'][3]
        try:
            self.conn = odbc.connect('Driver={SQL Server Native Client 11.0};'
                                     'MultipleActiveResultSets={True};'
                                     'Server=MAXIMUS2;'
                                     'username = mabbas;'
                                     'password = ninjaX3@;'
                                     'Database=CRW_YT;'
                                     'Trusted_Connection=yes;'
                                     )
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.sql_del,(self.del_vid_id))
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except Exception as ex_del:
            print('video could not be deleted: ', ex_del)
        pass
    # def save_to_DB(self,orig_url, vid_data):
    #     self.orig_url = orig_url
    #     self.vid_data = vid_data
    #     self.pattern = r'https://www.youtube.com/watch?v='
    #     self.sequence = self.orig_url
    #     if self.orig_url is None or re.search(self.pattern[:29], self.sequence[:29]) is None:
    #         orig_url = 'https://www.youtube.com/watch?v=4VfqVpTz4Q4'
    #     self.source_id = self.orig_url[len(orig_url) - 11:]
    #     self.df = pd.DataFrame(columns=['source_id', 'related_id', 'stamp_date'])
    #     try:
    #         self.conn = odbc.connect('Driver={SQL Server Native Client 11.0};'
    #                                  'MultipleActiveResultSets={True};'
    #                             'Server=MAXIMUS2;'
    #                             'username = mabbas;'
    #                             'password = ninjaX3@;'
    #                             'Database=CRW_YT;'
    #                             'Trusted_Connection=yes;'
    #                             )
    #         self.cursor = self.conn.cursor()
    #
    #     except:
    #         print('Error connecting to the database, please try again')
    #     try:
    #         if self.vid_data is None:
    #             print('no value retrieved from the link')
    #             raise ValueError('Did not received any data from the link')
    #         self.index = 0
    #         for self.key, self.value in self.vid_data.items():
    #             self.time_stamp = (
    #                     str(t.gmtime().tm_year) + '-' + str(t.gmtime().tm_mon) + '-' + str(t.gmtime().tm_mday) + ' ' + str(
    #                 t.gmtime().tm_hour) + ':' + str(t.gmtime().tm_min) + ':' + str(t.gmtime().tm_sec))
    #             self.df.loc[self.index] = [self.source_id, self.value[len(self.value) - 11:], self.time_stamp]
    #             self.index += 1
    #
    #             self.flag = 'N'
    #             self.sql = ' DECLARE @EXIST_FLAG char(1)' \
    #                   ' EXEC	[dbo].[GET_VIDEXIST]' \
    #                   ' @SOURCE_ID = ?,' \
    #                   ' @RELATED_ID = ?,' \
    #                   ' @EXIST_FLAG = @EXIST_FLAG OUTPUT;' \
    #                   ' SELECT @EXIST_FLAG'
    #
    #             self.values = (self.source_id, self.value[len(self.value) - 11:])
    #             self.cursor.execute(self.sql, (self.source_id, self.value[len(self.value) - 11:]))
    #             self.flag = self.cursor.fetchone()
    #             print('flag value: ',self.flag[0])
    #             if self.flag[0] == 'Y':
    #                 print(f'Video combination already in the database: {self.values[0]} and {self.values[1]}')
    #                 continue
    #             else:
    #                 pass
    #             print(f'Inserting video id`s in the database: {self.values[0]} and {self.values[1]}')
    #             self.cursor.execute('INSERT INTO dbo.YT_RELATED_VIDS (source_vid_id,related_vid_id,time_stamp) values (?,?,?)',
    #                            (self.source_id, self.value[len(self.value) - 11:], self.time_stamp))
    #
    #         self.conn.commit()
    #         self.conn.close()
    #         print('saved relational video ids: ',self.source_id)
    #
    #     except Exception as Exx :
    #         print('Error Inserting Video id to the database, please try again: ', Exx)


    def get_next_related_video_id(self):
        try:
            self.conn = odbc.connect('Driver={SQL Server Native Client 11.0};'
                                'Server=MAXIMUS2;'
                                'username = mabbas;'
                                'password = ninjaX3@;'
                                'Database=CRW_YT;'
                                'Trusted_Connection=yes;'
                                )
            self.cursor = self.conn.cursor()

        except:
            print('Error connecting to the database, please try again')
        self.next_video_id_sql = ' DECLARE @next_vid_id varchar(12) ' \
                            ' EXEC	[dbo].GET_NEXT_VID_ID ' \
                            ' @VIDEO_ID = @next_vid_id OUTPUT; ' \
                            ' SELECT @next_vid_id'
        self.cursor.execute(self.next_video_id_sql)
        self.next_vid_id = self.cursor.fetchone()[0]
        self.conn.close()
        return self.next_vid_id