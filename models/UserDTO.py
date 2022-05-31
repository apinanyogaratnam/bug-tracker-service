from typing import Set


class UserDTO:
    def __init__(self, internal_user_id: int, external_user_id: str, username: str, email: str, project_ids: Set[int], created_at: str) -> None:
        self.internal_user_id = internal_user_id
        self.external_user_id = external_user_id
        self.username = username
        self.email = email
        self.project_ids = project_ids
        self.created_at = created_at
