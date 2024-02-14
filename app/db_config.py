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
                return cur.fetchall()
            else:
                return None

# Access environment variables


# def get_db():
#     conn = None
#     try:
#         # Connect to your database
#         conn = psycopg2.connect(
#             database=pg_database,
#             user=pg_user,
#             password=pg_password,
#             host=pg_host,
#             port=pg_port
#         )

#         print("Database connection successfully")
#         return conn

#     except Exception as e:
#         print(e)
#         raise HTTPException(
#             status_code=500, detail="Database connection failed.")
#     finally:
#         if conn is not None:
#             conn.close()
