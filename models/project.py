from typing import List, Set

from controllers.utility import Utility
from models import Column


class Project:
    def __init__(
        self: 'Project',
        user_id: int,
        administrator_id: int,
        co_administrator_ids: Set[int],
        member_ids: Set[int],
        name: str,
        description: str,
        project_id: int | None = None,
        created_at: str | None = None,
    ) -> None:
        self.project_id = project_id
        self.user_id = user_id
        self.administrator_id = administrator_id
        self.co_administrator_ids = co_administrator_ids
        self.member_ids = member_ids
        self.name = name,
        self.description = description
        self.created_at = created_at

    def create(self: 'Project') -> 'Project':
        """Creates a new user in the database

        Args:
            self (User): the user class object

        Raises:
            Exception: if write query fails
        """
        utility_handler = Utility()

        save_project_query: str = '''
            INSERT INTO projects (
                user_id,
                administrator_id,
                co_administrator_ids,
                member_ids,
                name,
                description
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            ) RETURNING project_id, created_at;
        '''

        records_to_insert = (
            self.user_id,
            self.administrator_id,
            self.co_administrator_ids,
            self.member_ids,
            self.name,
            self.description,
        )

        returned_project: List[tuple] = utility_handler.write_to_postgres_structured(save_project_query, records_to_insert)

        if returned_project:
            self.project_id = returned_project[0][0]
            self.created_at = returned_project[0][1].strftime('%Y-%m-%d %H:%M:%S')

        return self

    def jsonify(self: 'Project') -> dict:
        """Converts the user class object to a dictionary

        Args:
            self (User): the user class object

        Returns:
            dict: the user class object as a dictionary
        """
        return {
            'project_id': self.project_id,
            'user_id': self.user_id,
            'administrator_id': self.administrator_id,
            'co_administrator_ids': self.co_administrator_ids,
            'member_ids': self.member_ids,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at
        }

    def get_columns(self: 'Project', project_id: int) -> List[Column]:
        query_user: str = f'''
            SELECT
                column_id,
                project_id,
                raw_columns,
                EXTRACT(EPOCH FROM created_at) AS created_at
            FROM columns
            WHERE project_id = '{project_id}';
        '''

        utility_handler = Utility()

        queried_columns: list = utility_handler.create_pandas_table(query_user).to_dict(orient='records')

        columns: list = list(map(lambda column: Column(**column), queried_columns))
        return columns
