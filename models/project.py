from typing import List, Set

from controllers.utility import Utility


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

    def create(self: 'Project', test_mode: bool = False) -> 'Project':
        """Creates a new user in the database

        Args:
            self (User): the user class object

        Raises:
            Exception: if write query fails
        """
        utility_handler = Utility()

        if test_mode:
            save_project_query: str = '''
                INSERT INTO projects (
                    project_id,
                    user_id,
                    administrator_id,
                    co_administrator_ids,
                    member_ids,
                    name,
                    description
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                ) RETURNING *;
            '''

            records_to_insert = (
                self.project_id,
                self.user_id,
                self.administrator_id,
                self.co_administrator_ids,
                self.member_ids,
                self.name,
                self.description,
            )
        else:
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
            print(save_project_query)

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
            self.created_at = returned_project[0][1]

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
