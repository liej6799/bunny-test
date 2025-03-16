drop view if exists vw_video_library;

CREATE VIEW vw_video_library AS

select a.* from tb_refresh_video_library as a
inner join tb_flow as b on a.flow_id = b.flow_id
where (b.timestamp) = (
select max((a.timestamp))
    from tb_flow as a 
	inner join tb_flow as b on a.flow_id = b.flow_id
	and a.status = 'START_FLOW' and b.status = 'END_FLOW'
    and a.flow_name = 'REFRESH_VIDEO_LIBRARY' and b.flow_name = 'REFRESH_VIDEO_LIBRARY'
    limit 1
)
