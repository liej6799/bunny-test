

CREATE TABLE IF NOT EXISTS tb_flow
(
    timestamp TIMESTAMPTZ NOT NULL,
    flow_name TEXT,
    flow_id uuid,
    status TEXT
);