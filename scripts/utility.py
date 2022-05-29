import os

import psycopg2

from dotenv import load_dotenv

load_dotenv()


def get_postgres_connection():
    host = os.environ.get('POSTGRES_HOST')
    database = os.environ.get('POSTGRES_DATABASE')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')

    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    return connection
