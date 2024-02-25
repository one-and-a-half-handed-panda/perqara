CREATE TABLE IF NOT EXISTS(
    user_id     UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_age    SMALLINT    NOT NULL,
    user_name   TEXT        NOT NULL
);