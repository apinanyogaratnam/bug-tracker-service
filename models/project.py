from typing import Set

from controllers.utility import Utility


class Project:
    def __init__(
        self: 'Project',
        project_id: int,
        user_id: int,
        administrator_id: int,
        co_administrator_ids: Set[int],
        member_ids: Set[int],
        name: str,
        description: str,
        created_at: str
    ) -> None:
        self.project_id = project_id
        self.user_id = user_id
        self.administrator_id = administrator_id
        self.co_administrator_ids = co_administrator_ids
        self.member_ids = member_ids
        self.name = name,
        self.description = description
        self.created_at = created_at

    def create(self: 'Project'):
        """Creates a new user in the database

        Args:
            self (User): the user class object

        Raises:
            Exception: if write query fails
        """
        utility_handler = Utility()

        save_user_query: str = '''
            INSERT INTO projects (
                project_id,
                user_id,
                administrator_id,
                co_administrator_ids,
                member_ids,
                name,
                description
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            );
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

        utility_handler.write_to_postgres_structured(save_user_query, records_to_insert)
