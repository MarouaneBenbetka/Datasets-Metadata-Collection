-- Indexes for datasets
CREATE INDEX idx_datasets_source_id ON datasets(source_id);
CREATE INDEX idx_datasets_stats_id ON datasets(stats_id);
CREATE INDEX idx_datasets_license_id ON datasets(license_id);
CREATE INDEX idx_datasets_title ON datasets(title);
CREATE INDEX idx_datasets_url ON datasets(url);
-- Composite index for dataset owners
CREATE INDEX idx_dataset_owners_on_owner_and_dataset ON dataset_owners(owner_id, dataset_id);
-- Indexes on tags and use cases by name
CREATE INDEX idx_tags_name ON tags(name);
CREATE INDEX idx_use_cases_name ON use_cases(name);
-- Indexes for features table
CREATE INDEX idx_features_dataset_id ON features(dataset_id);
CREATE INDEX idx_features_name ON features(name);
-- Indexes for notebooks and issues on dataset_id
CREATE INDEX idx_notebooks_dataset_id ON notebooks(dataset_id);
CREATE INDEX idx_issues_dataset_id ON issues(dataset_id);
-- Index for discussions on dataset_id
CREATE INDEX idx_discussions_dataset_id ON discussions(dataset_id);
-- Index for sources name (optimized for low cardinality)
CREATE INDEX idx_sources_name ON sources(name);