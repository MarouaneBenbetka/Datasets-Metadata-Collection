from app.db_config import run_query


CREATE_TABLES_SQL = """

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;


CREATE TYPE  sources_enum AS ENUM ('Github', 'Kaggle', 'UCI-ML-Repo' , 'Hugging Face' );

CREATE TABLE IF NOT EXISTS sources (
    id SERIAL PRIMARY KEY,
    name sources_enum NOT NULL UNIQUE,
    url VARCHAR(255)  ,
    description TEXT
);

CREATE TABLE IF NOT EXISTS licenses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) ,
    url VARCHAR(255) UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS stats (
    id SERIAL PRIMARY KEY,
    views_count INT DEFAULT 0  CHECK (views_count >= 0),
    likes_count INT DEFAULT 0  CHECK (likes_count >= 0),
    download_count INT DEFAULT 0  CHECK (download_count >= 0)
);

CREATE TABLE IF NOT EXISTS owners (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) ,
    profile_url VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS use_cases (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS datasets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL UNIQUE,
    ref VARCHAR(255),
    description TEXT,
    total_bytes BIGINT CHECK (total_bytes >= 0),
    source_id INT REFERENCES sources(id) ON DELETE CASCADE,
    stats_id INT REFERENCES stats(id) ON DELETE CASCADE,
    license_id INT REFERENCES licenses(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS dataset_owners (
    id SERIAL PRIMARY KEY,
    owner_id INT REFERENCES owners(id) ON DELETE CASCADE,
    dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
    UNIQUE (owner_id, dataset_id)
);

CREATE TABLE IF NOT EXISTS dataset_tags (
    dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
    tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, tag_id)
);

CREATE TABLE IF NOT EXISTS dataset_use_cases (
    dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
    use_case_id INT REFERENCES use_cases(id) ON DELETE CASCADE,
    PRIMARY KEY (dataset_id, use_case_id)
);

CREATE TABLE IF NOT EXISTS features (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type TEXT ,
    description TEXT,
    dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS notebooks (
    id SERIAL PRIMARY KEY,
    dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
    ref VARCHAR(255),
    url VARCHAR(255) ,
    author VARCHAR(255) ,
    last_run_time DATE,
    total_votes INT DEFAULT 0  CHECK (total_votes >= 0),
    language VARCHAR(255) ,
    content JSON
);

CREATE TABLE IF NOT EXISTS issues (
    id SERIAL PRIMARY KEY,
    dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
    title VARCHAR(255) ,
    body TEXT ,
    url VARCHAR(255) ,
    creation_date DATE ,
    updated_date DATE,
    reactions JSON,
    comments JSON
);

CREATE TABLE IF NOT EXISTS discussions (
    id SERIAL PRIMARY KEY,
    dataset_id INT REFERENCES datasets(id) ON DELETE CASCADE,
    title VARCHAR(255) ,
    content TEXT ,
    url VARCHAR(255) ,
	user_name VARCHAR(255) ,
    comments JSON
);
"""


async def create_schema():
    run_query(CREATE_TABLES_SQL)
