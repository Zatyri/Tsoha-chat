CREATE TABLE IF NOT EXISTS users
(
    id SERIAL NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    uuid character varying NOT NULL,
    role integer NOT NULL DEFAULT 1,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)