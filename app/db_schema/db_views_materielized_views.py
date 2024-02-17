from app.db_config import run_query


VIEWS_CREATION_SQL = """


-- View: Dataset Overview
-- Provides a quick overview of datasets including their source, license, and basic statistics.
CREATE VIEW dataset_overview AS
SELECT d.id, d.title, s.name AS source, l.name AS license, st.views_count, st.likes_count, st.download_count
FROM datasets d
JOIN sources s ON d.source_id = s.id
LEFT JOIN licenses l ON d.license_id = l.id
JOIN stats st ON d.stats_id = st.id;

-- View: Dataset Tags and Use Cases
-- Aggregates all tags and use cases associated with each dataset for easy filtering and searching.
CREATE VIEW dataset_tags_use_cases AS
SELECT d.id AS dataset_id, d.title, array_agg(t.name) AS tags, array_agg(u.name) AS use_cases
FROM datasets d
LEFT JOIN dataset_tags dt ON d.id = dt.dataset_id
LEFT JOIN tags t ON dt.tag_id = t.id
LEFT JOIN dataset_use_cases duc ON d.id = duc.dataset_id
LEFT JOIN use_cases u ON duc.use_case_id = u.id
GROUP BY d.id;

-- Materialized View: Most Popular Datasets
-- Keeps a cached list of the most popular datasets based on views, likes, and downloads.
-- Useful for reducing computation time for frequently accessed statistics on dataset popularity.
CREATE MATERIALIZED VIEW most_popular_datasets AS
SELECT d.id, d.title, s.name AS source, st.views_count, st.likes_count, st.download_count
FROM datasets d
JOIN stats st ON d.stats_id = st.id
JOIN sources s ON d.source_id = s.id
ORDER BY st.views_count DESC, st.likes_count DESC, st.download_count DESC
LIMIT 100;

-- Materialized View: Dataset Details by Owner
-- Aggregates datasets along with their owners for a comprehensive view that includes ownership information.
-- Useful for enhancing data accessibility by associating datasets with their respective owners.
CREATE MATERIALIZED VIEW dataset_details_by_owner AS
SELECT o.name AS owner_name, o.profile_url, d.title, d.url, d.description
FROM dataset_owners dow
JOIN owners o ON dow.owner_id = o.id
JOIN datasets d ON dow.dataset_id = d.id;



"""


async def create_views():
    run_query(VIEWS_CREATION_SQL)
