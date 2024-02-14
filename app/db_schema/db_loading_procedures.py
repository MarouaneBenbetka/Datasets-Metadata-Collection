from app.db_config import run_query


LOAD_PROCEDURE_SQL = """
CREATE OR REPLACE FUNCTION insert_data(json_data JSONB)
RETURNS VOID AS $$
DECLARE
    dataset_item JSONB;
	owner_item JSONB;
	use_case_item JSONB;
    source_id INT;
    stats_id INT;
    license_id INT;
    last_dataset_id INT;
    owner_id INT;
    tag_item varchar(255);
    feature_item JSONB;
    use_case_id INT;
    notebook_item JSONB;
    discussion_item JSONB;
    issue_item JSONB;
BEGIN
    -- Loop through each dataset in the input JSON array
    FOR dataset_item IN SELECT * FROM jsonb_array_elements(json_data) LOOP
        
        -- Insert Source
        INSERT INTO sources (name, url, description)
        VALUES ((dataset_item->'source'->>'name')::sources_enum, dataset_item->'source'->>'url', dataset_item->'source'->>'description')
        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id INTO source_id;

        -- Insert Stats
        INSERT INTO stats (views_count, likes_count, download_count)
        VALUES ((dataset_item->'stats'->>'views_count')::INT, (dataset_item->'stats'->>'likes_count')::INT, (dataset_item->'stats'->>'download_count')::INT)
        RETURNING id INTO stats_id;

        -- Insert License
        INSERT INTO licenses (name, url, description)
        VALUES (dataset_item->'License'->>'name', dataset_item->'License'->>'url', dataset_item->'License'->>'description')
        ON CONFLICT (url) DO UPDATE SET name = EXCLUDED.name RETURNING id INTO license_id;

        -- Insert Dataset
        INSERT INTO datasets (title, url, description, total_bytes, source_id, stats_id, license_id)
        VALUES (dataset_item->>'title', dataset_item->>'url', dataset_item->>'description', (dataset_item->>'totalBytes')::BIGINT, source_id, stats_id, license_id)
        ON CONFLICT (url) DO UPDATE SET stats_id = EXCLUDED.stats_id
		RETURNING id INTO last_dataset_id;

        -- Insert Owners (Assuming many to many relationship)
        FOR owner_item IN SELECT * FROM jsonb_array_elements(dataset_item->'owners') LOOP
            INSERT INTO owners (name, profile_url)
            VALUES (owner_item->>'name', owner_item->>'url')
            ON CONFLICT (profile_url) DO UPDATE SET name = EXCLUDED.name RETURNING id INTO owner_id;

            INSERT INTO dataset_owners (owner_id, dataset_id)
            VALUES (owner_id, last_dataset_id)
            ON CONFLICT DO NOTHING;
        END LOOP;

        -- Insert Tags (Assuming many to many relationship)
        FOR tag_item IN SELECT * FROM jsonb_array_elements(dataset_item->'tags') LOOP
            INSERT INTO tags (name)
            VALUES (tag_item)
            ON CONFLICT (name) DO NOTHING;

            INSERT INTO dataset_tags (dataset_id, tag_id)
            SELECT last_dataset_id, id FROM tags WHERE name = tag_item
			ON CONFLICT DO NOTHING;
        END LOOP;

        -- Insert Features
        FOR feature_item IN SELECT * FROM jsonb_array_elements(dataset_item->'features') LOOP
            INSERT INTO features (name, type, description, dataset_id)
            VALUES (feature_item->>'name', feature_item->>'type', feature_item->>'description', last_dataset_id);
        END LOOP;

        -- Insert Use Cases
        FOR use_case_item IN SELECT * FROM jsonb_array_elements(dataset_item->'useCases') LOOP
            INSERT INTO use_cases (name, description)
            VALUES (use_case_item->>'name', use_case_item->>'description')
            ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description RETURNING id INTO use_case_id;

            INSERT INTO dataset_use_cases (dataset_id, use_case_id)
            SELECT last_dataset_id, id FROM use_cases WHERE name = use_case_item->>'name'
			ON CONFLICT DO NOTHING;
        END LOOP;

        -- Insert Notebooks
        FOR notebook_item IN SELECT * FROM jsonb_array_elements(dataset_item->'notebooks') LOOP
            INSERT INTO notebooks (dataset_id, ref, url, author, last_run_time, total_votes, language)
            VALUES (
                last_dataset_id,
                notebook_item->>'ref',
                notebook_item->>'url',
                notebook_item->>'author',
                (notebook_item->>'last_run_time')::DATE,
                (notebook_item->>'total_votes')::INT,
                notebook_item->>'language'
		       
            );
        END LOOP;

        -- Insert Discussions
        FOR discussion_item IN SELECT * FROM jsonb_array_elements(dataset_item->'descussions') LOOP
            INSERT INTO discussions (dataset_id, title, content, url, user_name, comments)
            VALUES (
                last_dataset_id,
                discussion_item->>'title',
                discussion_item->>'content',
                discussion_item->>'url',
                discussion_item->>'user',
                discussion_item->'comments'
            );
        END LOOP;

        -- Insert Issues
        FOR issue_item IN SELECT * FROM jsonb_array_elements(dataset_item->'issues') LOOP
            INSERT INTO issues (dataset_id, title, body, url, creation_date, updated_date, reactions, comments)
            VALUES (
                last_dataset_id,
                issue_item->>'title',
                issue_item->>'body',
                issue_item->>'url',
                (issue_item->>'creation_date')::DATE,
                (issue_item->>'updated_date')::DATE,
                issue_item->'reactions',
                issue_item->'comments'
            );
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

"""


async def create_loading_procedure():
    run_query(LOAD_PROCEDURE_SQL)
