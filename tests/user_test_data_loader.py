from datetime import datetime
from typing import List

from models import User


class UserTestDataLoader:
    def __init__(self: 'UserTestDataLoader') -> None:
        pass

    def users(self: 'UserTestDataLoader') -> List[User]:
        return [
            User(
                internal_user_id=1,
                external_user_id='external_user_id',
                username='username',
                email='email',
                created_at=datetime.utcnow(),
            ),
            User(
                internal_user_id=2,
                external_user_id='external_user_id_1',
                username='username1',
                email='email1',
                created_at=datetime.utcnow(),
            ),
        ]

    def initialize_database(self: 'UserTestDataLoader') -> None:
        users: List[User] = self.users()

        for user in users:
            user.create()


if __name__ == '__main__':
    UserTestDataLoader().initialize_database()
