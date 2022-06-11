import os

import pandas as pd
import psycopg2
import redis

from dotenv import load_dotenv

load_dotenv()


class BaseAPI:
    def __init__(self: 'BaseAPI') -> None:
        self.utility_handler: Utility = Utility()
        self.is_caching_enabled: bool = os.getenv('IS_CACHING_ENABLED', True)
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=os.getenv('REDIS_PORT', 6379),
            db=0
        )

    def create_pandas_table(self: 'BaseAPI', sql_query) -> pd.DataFrame:
        with self.utility_handler.get_postgres_connection() as connection:
            table = pd.read_sql_query(sql_query, connection)

        return table

    def set_cache(self: 'BaseAPI', key: str, value: str, expiry: int | None = None) -> None:
        if self.is_caching_enabled:
            self.redis_client.set(key, value, expiry)

    def get_cache(self: 'BaseAPI', key: str) -> str | None:
        if self.is_caching_enabled:
            return self.redis_client.get(key)


class Utility:
    def __init__(self: 'Utility') -> None:
        pass

    @staticmethod
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

    def write_to_postgres(self: 'Utility', sql_query: str) -> None:
        with self.get_postgres_connection() as connection, connection.cursor() as cursor:
            try:
                cursor.execute(sql_query)
                connection.commit()
            except Exception as error:
                print(error)
                connection.rollback()
                raise Exception(f'Failed to write to database {sql_query}')

    def write_to_postgres_structured(self: 'Utility', sql_query: str, records_to_insert: tuple) -> dict | list | None:
        with self.get_postgres_connection() as connection, connection.cursor() as cursor:
            try:
                cursor.execute(sql_query, records_to_insert)
                connection.commit()

                try:
                    data = cursor.fetchall()
                except Exception as error:
                    print(error)
                    data = None
            except Exception as error:
                connection.rollback()
                raise Exception(f'write to postgres structured failed {str(error)}')

        return data
