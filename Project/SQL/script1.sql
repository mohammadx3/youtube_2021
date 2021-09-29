use crw_yt;
go

SELECT count(1) from dbo.YT_VIDEO_DETAILS 
select count(1)from dbo.YT_CHANNEL_DETAILS 
select count(1)from dbo.YT_RELATED_VIDS
--select distinct * from YT_RELATED_VIDS
--select * from dbo.YT_RELATED_VIDS where source_vid_id = 'RqepKuZ5PZE'
select * from dbo.YT_RELATED_VIDS
SELECT * from dbo.YT_VIDEO_DETAILS 

select related_vid_id from dbo.YT_RELATED_VIDS where related_vid_id not in (select source_vid_id from dbo.YT_RELATED_VIDS)
and related_vid_id not in (SELECT VIDEO_ID from dbo.YT_VIDEO_DETAILS)
select distinct related_vid_id from dbo.YT_RELATED_VIDS where  not exists (SELECT 1 from dbo.YT_VIDEO_DETAILS where VIDEO_ID = related_vid_id )