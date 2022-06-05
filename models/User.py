from typing import Set

from controllers.utility import Utility


class User:
    def __init__(
        self: 'User',
        external_user_id: str,
        username: str,
        email: str,
        project_ids: Set[int],
        internal_user_id: int = None,
        created_at: str = None,
    ) -> None:
        self.internal_user_id = internal_user_id
        self.external_user_id = external_user_id
        self.username = username
        self.email = email
        self.project_ids = project_ids
        self.created_at = created_at

    def create(self: 'User', test_mode: bool = False) -> 'User':
        """Creates a new user in the database

        Args:
            self (User): the user class object

        Raises:
            Exception: if write query fails
        """
        utility_handler = Utility()

        if test_mode:
            save_user_query: str = '''
                INSERT INTO users (
                    internal_user_id,
                    external_user_id,
                    username,
                    email,
                    project_ids
                ) VALUES (
                    %s, %s, %s, %s, %s
                );
            '''

            records_to_insert = (self.internal_user_id, self.external_user_id, self.username, self.email, self.project_ids)
        else:
            save_user_query: str = '''
                INSERT INTO users (
                    external_user_id,
                    username,
                    email,
                    project_ids
                ) VALUES (
                    %s, %s, %s, %s
                ) RETURNING internal_user_id;
            '''

            records_to_insert = (self.external_user_id, self.username, self.email, self.project_ids)

        utility_handler.write_to_postgres_structured(save_user_query, records_to_insert)

        return self

    def jsonify(self: 'User') -> dict:
        """Returns a jsonified version of the user object

        Args:
            self (User): the user class object

        Returns:
            dict: the jsonified user object
        """
        return {
            'internal_user_id': self.internal_user_id,
            'external_user_id': self.external_user_id,
            'username': self.username,
            'email': self.email,
            'project_ids': self.project_ids,
            'created_at': self.created_at,
        }
