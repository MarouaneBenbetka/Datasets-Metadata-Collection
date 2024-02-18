from fastapi import APIRouter, HTTPException
from typing import List
import json  # Assuming your run_query returns JSON serializable results
from ..db_config import run_query

router = APIRouter()


@router.get("/stats/sources")
async def get_sources_statistics():
    # Query for number of datasets per source
    datasets_per_source_query = """
    SELECT s.name, COUNT(d.id) AS dataset_count
    FROM sources s
    LEFT JOIN datasets d ON s.id = d.source_id
    GROUP BY s.name
    ORDER BY dataset_count DESC;
    """

    try:
        datasets_per_source = run_query(datasets_per_source_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "datasets_per_source": datasets_per_source,
    }


@router.get("/stats/tags")
async def get_tags_statistics():

    # Query for most searched tags
    most_searched_tags_query = """
    SELECT t.name, COUNT(dt.dataset_id) AS usage_count
    FROM tags t
    JOIN dataset_tags dt ON t.id = dt.tag_id
    GROUP BY t.name
    ORDER BY usage_count DESC
    LIMIT 10;
    """

    try:
        most_searched_tags = run_query(most_searched_tags_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "most_searched_tags": most_searched_tags
    }
