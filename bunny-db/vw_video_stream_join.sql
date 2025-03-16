drop view if exists vw_video_stream_join;

CREATE VIEW vw_video_stream_join AS


select a.*,
b.captions_path,
b.seek_path,
b.thumbnail_path,
b.fallback_url,
b.video_playlist_url,
b.preview_url
from vw_video as a
inner join vw_video_stream as b on a.id = b.id

