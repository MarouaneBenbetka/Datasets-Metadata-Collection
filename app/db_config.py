import psycopg2

from fastapi import HTTPException
from dotenv import load_dotenv
from psycopg2.extras import DictCursor
import os
# Database connection paameters


# Load environment variables from .env file
load_dotenv()
pg_database = os.environ.get("DB_NAME")
pg_user = os.environ.get("DB_USERNAME")
pg_password = os.environ.get("DB_PASSWORD")
pg_host = os.environ.get("HOST")
pg_port = os.environ.get("PORT")


def run_query(sql, params=None):

    # Establish connection
    with psycopg2.connect(database=pg_database, user=pg_user, password=pg_password, host=pg_host, port=pg_port) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, params)

            # If the SQL command is a SELECT statement, fetch the results
            if cur.description:
                result = [dict(row) for row in cur.fetchall()]
                return result
            else:
                return None

# Access environment variables
