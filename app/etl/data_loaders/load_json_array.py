
from app.db_config import run_query


async def load_multiple_json(json):
    run_query(f"SELECT insert_data(%s)", (json,))
