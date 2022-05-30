import os

import pandas as pd
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


class BaseAPI:
    def __init__(self: 'BaseAPI') -> None:
        pass

    def create_pandas_table(self: 'BaseAPI', sql_query) -> pd.DataFrame:
        with get_postgres_connection() as connection:
            table = pd.read_sql_query(sql_query, connection)

        return table


class Utility:
    def __init__(self: 'Utility') -> None:
        pass
