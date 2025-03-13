

CREATE TABLE IF NOT EXISTS tb_refresh_video_library
(
    timestamp TIMESTAMPTZ NOT NULL,
    id INTEGER, 
    name TEXT, 
    video_count INTEGER,
    traffic_usage INTEGER,
    storage_usage INTEGER,
    date_created DATE
);