import json

from typing import List

from controllers.utility import Utility


class Column:
    def __init__(
        self: 'Column',
        column_id: int,
        project_id: int,
        raw_columns: dict,
        created_at: str | None = None,
    ) -> None:
        self.column_id = column_id
        self.project_id = project_id
        self.raw_columns = raw_columns
        self.created_at = created_at

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
                project_id,
                raw_columns
            ) VALUES (
                %s, %s
            ) RETURNING column_id, created_at;
        '''

        records_to_insert = (
            self.project_id,
            json.dumps(self.raw_columns),
        )

        returned_project: List[tuple] = utility_handler.write_to_postgres_structured(save_column_query, records_to_insert)

        if returned_project:
            self.column_id = returned_project[0][0]
            self.created_at = returned_project[0][1].strftime('%Y-%m-%d %H:%M:%S')

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
