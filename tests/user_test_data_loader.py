from typing import Set

from models import User


class UserTestDataLoader:
    def __init__(self: 'UserTestDataLoader') -> None:
        pass

    def users(self: 'UserTestDataLoader') -> Set[User]:
        return set([
            User(
                internal_user_id=1,
                external_user_id='external_user_id',
                username='username',
                email='email',
                project_ids=[1, 2, 3],
                created_at='created_at'
            ),
            User(
                internal_user_id=2,
                external_user_id='external_user_id_1',
                username='username1',
                email='email1',
                project_ids=[4, 5, 6],
                created_at='created_at_1'
            ),
        ])

    def initialize_database(self: 'UserTestDataLoader') -> None:
        users: Set[User] = self.users()

        for user in users:
            user.create()


if __name__ == '__main__':
    UserTestDataLoader().initialize_database()
