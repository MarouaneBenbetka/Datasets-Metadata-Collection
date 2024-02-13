import os
import urllib.parse as up
from dotenv import load_dotenv
import psycopg2
import json

# Load environment variables from .env file
load_dotenv()

# Access environment variables
pg_database = os.environ.get("PG_DATABASE")
pg_user = os.environ.get("PG_USER")
pg_password = os.environ.get("PG_PASSWORD")
pg_host = os.environ.get("PG_HOST")
pg_port = os.environ.get("PG_PORT")

# Create PostgreSQL connection
up.uses_netloc.append("postgres")
url = up.urlparse(
    f"postgres://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}")

try:
    # Attempt to establish a connection
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    # Create a cursor to execute SQL queries
    cursor = conn.cursor()

    # Read JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Call the stored procedure to insert data
    cursor.execute("SELECT insert_data(%s)", (json.dumps(data),))

    # Commit the transaction
    conn.commit()

    print("Data inserted successfully.")

except psycopg2.Error as e:
    # If an error occurs during connection, query execution, or transaction, print the error message
    print(f"Error: {e}")

finally:
    # Close the cursor and connection in the finally block to ensure they're always closed
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        print("Connection closed.")
