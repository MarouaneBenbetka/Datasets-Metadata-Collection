from fastapi import APIRouter, Request, HTTPException, Query
from typing import Optional, List
from ..db_config import run_query

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


@router.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: int):

    if not dataset_id:
        raise HTTPException(status_code=400, detail="Invalid dataset ID")

    query = f"""
                SELECT
                    d.* ,

                    COALESCE(array_agg(
                            json_build_object(
                                'owner_id', o.id,
                                'owner_name', o.name,
                                'owner_url', o.profile_url
                            ) ) FILTER (WHERE o.id IS NOT NULL), '{{}}') AS owners ,
                    
                    CASE 
                        WHEN (license_id IS NOT NULL ) THEN json_build_object(
                        'license_id', l.id,
                        'license_name', l.name,
                        'license_url', l.url
                        )
                        ELSE 'null' 
                    END AS license ,

                    CASE 
                        WHEN (stats_id IS NOT NULL ) THEN json_build_object(
                        'views_count', s.views_count,
                        'likes_count', s.likes_count,
                        'download_count', s.download_count
                        )
                        ELSE 'null' 
                    END AS stats
                    
                    
                FROM
                    datasets d
                    LEFT JOIN licenses l ON d.license_id = l.id
                    LEFT JOIN dataset_owners dow ON d.id = dow.dataset_id
                    LEFT JOIN owners o ON dow.owner_id = o.id
                    LEFT JOIN stats s ON d.stats_id = s.id
                WHERE
                    d.id = {dataset_id} 
                GROUP BY
                    d.id, l.id, s.id;
            """
    try:
        print(dataset_id)
        print("check")
        dataset_details = run_query(query)
        if not dataset_details:
            raise HTTPException(status_code=404, detail="Dataset not found")
        return dataset_details
    except Exception as e:
        print(e)
        # Log the exception details here, e.g., print(e)
        raise HTTPException(
            status_code=500, detail="An error occurred while fetching the dataset details.")


#  dataset_json = {
#             "id": first_row["id"],
#             "title": first_row["title"],
#             "url": first_row["url"],
#             "description": first_row["description"],
#             "license": {
#                 "name": first_row.get("license_name"),
#                 "url": first_row.get("license_url")
#             },
#             "owner": {
#                 "name": first_row.get("owner_name"),
#                 "profile_url": first_row.get("profile_url")
#             }
#         }
