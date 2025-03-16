

drop table if exists tb_refresh_video;

CREATE TABLE IF NOT EXISTS tb_refresh_video
(
    timestamp TIMESTAMPTZ NOT NULL,
    flow_id uuid,
    id uuid, 
    video_library_id INTEGER,
    name TEXT, 
    date_upload DATE,
    views INTEGER,
    encode_process INTEGER,
    storage_size INTEGER
);