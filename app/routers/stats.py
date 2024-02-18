from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import FileResponse
from typing import Optional, List
from ..db_config import run_query
from ..utils.jwt import verify_token
from ..utils.dataset_files import find_csv_in_folder
import os


router = APIRouter()


@router.get("/datasets")
async def get_datasets(
        limit: int = 10,
        page: int = 1,
        title: Optional[str] = None,
        source_id: Optional[int] = None,
        min_views: Optional[int] = None,
        min_likes: Optional[int] = None,
        min_downloads: Optional[int] = None,
        tags: Optional[List[str]] = Query(None)):  # Accepts a list of tags
    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400, detail="Invalid page or limit value.")

    query_params = []
    conditions = []

    if title:
        conditions.append("d.title ILIKE %s")
        query_params.append(f"%{title}%")
    if source_id:
        conditions.append("d.source_id = %s")
        query_params.append(source_id)
    if min_views:
        conditions.append("s.views_count >= %s")
        query_params.append(min_views)
    if min_likes:
        conditions.append("s.likes_count >= %s")
        query_params.append(min_likes)
    if min_downloads:
        conditions.append("s.download_count >= %s")
        query_params.append(min_downloads)

    where_clause = " AND ".join(conditions)
    where_clause = f"WHERE {where_clause}" if conditions else ""

    # Adjusting for tags requirement
    tags_join_and_filter_clause = ""
    if tags:
        # Create placeholders for tags
        tags_placeholder = ', '.join(['%s'] * len(tags))
        query_params.extend(tags)  # Add tags to query parameters
        tags_join_and_filter_clause = f"""
        AND d.id IN (
            SELECT dt.dataset_id
            FROM dataset_tags dt
            JOIN tags t ON dt.tag_id = t.id
            WHERE t.name ILIKE ANY (ARRAY[{tags_placeholder}])
            GROUP BY dt.dataset_id
            HAVING COUNT(DISTINCT t.name) = %s
        )
        """
        query_params.append(
            len(tags))  # Ensure the dataset matches the exact number of specified tags

    query = f"""
        SELECT DISTINCT d.id, d.title, d.url, d.description, s.views_count, s.likes_count, s.download_count
        FROM datasets d
        JOIN stats s ON d.stats_id = s.id
        {where_clause}
        {tags_join_and_filter_clause}
        ORDER BY d.id ASC
        LIMIT %s OFFSET %s;
    """
    query_params.extend([limit, (page - 1) * limit])

    try:
        # Assuming run_query is adapted to handle parameterized queries
        datasets = run_query(query, query_params)
        return datasets
    except Exception as e:
        print(e)
        return {"error": "An error occurred while fetching data."}
