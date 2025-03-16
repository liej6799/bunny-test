

CREATE TABLE IF NOT EXISTS tb_refresh_video_library
(
    timestamp TIMESTAMPTZ NOT NULL,
    flow_id uuid,
    id INTEGER, 
    name TEXT, 
    video_count INTEGER,
    traffic_usage INTEGER,
    storage_usage INTEGER,
    date_created DATE,
    api_key TEXT,
    read_only_api_key TEXT
);