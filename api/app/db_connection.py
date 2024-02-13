import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()


def establish_connection():
    try:
        connection = psycopg2.connect(host=os.environ.get('HOST'), port=os.environ.get('PORT'), database=os.environ.get(
            'DB_NAME'), user=os.environ.get('DB_USERNAME'), password=os.environ.get('DB_PASSWORD'), cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        return cursor
    except:
        raise Exception()
