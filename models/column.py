import json

from typing import List

from controllers.utility import Utility


class Column:
    def __init__(
        self: 'Column',
        project_id: int,
        raw_columns: dict | None = None,
        column_id: int | None = None,
        created_at: str | None = None,
    ) -> None:
        self.column_id = column_id
        self.project_id = project_id
        self.raw_columns = raw_columns
        self.created_at = created_at

        self.order_raw_columns()

    def create(self: 'Column') -> 'Column':
        """Creates a new column in the database

        Args:
            self (Column): the column class object

        Raises:
            Exception: if write query fails
        """
        utility_handler = Utility()

        save_column_query: str = '''
            INSERT INTO columns (
                project_id
            ) VALUES (
                %s
            ) RETURNING column_id, raw_columns, created_at;
        '''

        records_to_insert = (
            self.project_id
        )

        returned_column: List[tuple] = utility_handler.write_to_postgres_structured(save_column_query, records_to_insert)

        if returned_column:
            self.column_id = returned_column[0][0]
            self.raw_columns = returned_column[0][1]
            self.created_at = returned_column[0][2].strftime('%Y-%m-%d %H:%M:%S')

        return self

    def update(self: 'Column', raw_columns: dict) -> 'Column':
        utility_handler = Utility()

        update_column_query: str = '''
            UPDATE columns
            SET raw_columns = %s
            WHERE column_id = %s;
        '''

        records_to_update = (
            json.dumps(raw_columns),
            self.column_id,
        )

        utility_handler.write_to_postgres_structured(update_column_query, records_to_update)

        self.raw_columns = raw_columns

        return self

    def jsonify(self: 'Column') -> dict:
        """Converts the column class object to a dictionary

        Args:
            self (Column): the column class object

        Returns:
            dict: the column class object as a dictionary
        """
        return {
            'column_id': self.column_id,
            'project_id': self.project_id,
            'raw_columns': self.raw_columns,
            'created_at': self.created_at
        }

    def order_raw_columns(self: 'Column') -> None:
        """Orders the raw columns in the column class object

        Args:
            self (Column): the column class object
        """
        if self.raw_columns is None: return
        columns: dict = self.raw_columns
        sorted_columns: dict = dict(sorted(columns.items(), key=lambda x: int(x[0]), reverse=False))
        self.raw_columns = sorted_columns

    def get_last_column_id(self: 'Column') -> int:
        """Gets the last column id from raw_columns

        Args:
            self (Column): the column class object

        Raises:
            ValueError: if raw_columns is empty

        Returns:
            int: the last column id
        """
        raw_column_keys: list = [int(item) for item in self.raw_columns.keys()]
        return max(raw_column_keys)
