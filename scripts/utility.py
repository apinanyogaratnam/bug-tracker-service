import os

import psycopg2

from dotenv import load_dotenv

load_dotenv()


def get_postgres_connection() -> psycopg2.connect:
    host: str = os.environ.get('POSTGRES_HOST')
    database: str = os.environ.get('POSTGRES_DATABASE')
    user: str = os.environ.get('POSTGRES_USER')
    password: str = os.environ.get('POSTGRES_PASSWORD')

    connection: psycopg2.connect = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    return connection


def drop_table(table_name: str, connection: psycopg2.connect) -> None:
    with connection.cursor() as cursor:
        drop_table_query: str = f'DROP TABLE IF EXISTS {table_name}'
        cursor.execute(drop_table_query)
        connection.commit()
