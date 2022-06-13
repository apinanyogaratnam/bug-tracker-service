import json

from typing import List
from uuid import uuid4

from scripts.utility import get_postgres_connection, drop_table


def default_raw_columns_data() -> dict:
    sample_items: List[dict] = [
        {
            'id': str(uuid4()),
            'name': 'Sample card',
        },
        {
            'id': str(uuid4()),
            'name': 'You can move cards around in the board',
        },
        {
            'id': str(uuid4()),
            'name': 'Create a new card by clicking the + button',
        },
        {
            'id': str(uuid4()),
            'name': 'Delete a card by clicking the delete button',
        }
    ]

    return {
        'to_do': {
            'id': 1,
            'name': 'To Do',
            'items': sample_items,
        },
        'in_progress': {
            'id': 2,
            'name': 'In Progress',
            'items': [],
        },
        'done': {
            'id': 3,
            'name': 'Done',
            'items': [],
        },
    }


def main():
    TABLE_NAME: str = 'columns'

    with get_postgres_connection() as connection, connection.cursor() as cursor:
        drop_table(TABLE_NAME, connection)
        create_table_query: str = f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                column_id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
                project_id INT NOT NULL REFERENCES projects(project_id),
                raw_columns JSONB NOT NULL DEFAULT '{json.dumps(default_raw_columns_data())}',
                created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', NOW())
            );
        '''

        try:
            cursor.execute(create_table_query)
            connection.commit()
        except Exception as error:
            print(error)
            connection.rollback()


if __name__ == '__main__':
    main()
