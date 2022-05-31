from models.User import User
from models.UserDTO import UserDTO


class UserMapper:
    def __init__(self: 'UserMapper') -> None:
        pass

    def user_to_user_dto(self: 'UserMapper', user: User) -> UserDTO:
        return UserDTO(
            internal_user_id=user.internal_user_id,
            external_user_id=user.external_user_id,
            username=user.username,
            email=user.email,
            project_ids=user.project_ids,
            created_at=user.created_at
        )

    def user_dto_to_user(self: 'UserMapper', user_dto: UserDTO) -> User:
        return User(
            internal_user_id=user_dto.internal_user_id,
            external_user_id=user_dto.external_user_id,
            username=user_dto.username,
            email=user_dto.email,
            project_ids=user_dto.project_ids,
            created_at=user_dto.created_at
        )
