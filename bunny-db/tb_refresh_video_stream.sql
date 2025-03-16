
drop table if exists tb_refresh_video_stream;

CREATE TABLE IF NOT EXISTS tb_refresh_video_stream
(
    timestamp TIMESTAMPTZ NOT NULL,
    flow_id uuid,
    id UUID, 
    video_library_id INTEGER,

    captions_path TEXT, 
    seek_path TEXT,
    thumbnail_path TEXT,
    fallback_url TEXT,
    video_playlist_url TEXT,
    preview_url TEXT
);