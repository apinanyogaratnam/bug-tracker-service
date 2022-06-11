from datetime import datetime
from typing import Set

from models import Project


class ProjectTestDataLoader:
    def __init__(self: 'ProjectTestDataLoader') -> None:
        pass

    def projects(self: 'ProjectTestDataLoader') -> List[Project]:
        return [
            Project(
                project_id=1,
                user_id=1,
                administrator_id=1,
                co_administrator_ids=[],
                member_ids=[],
                name='Project 1',
                description='The first test project to be created',
                created_at=datetime.utcnow(),
            ),
            Project(
                project_id=2,
                user_id=1,
                administrator_id=1,
                co_administrator_ids=[],
                member_ids=[],
                name='Project 2',
                description='The second test project to be created',
                created_at=datetime.utcnow(),
            ),
            Project(
                project_id=3,
                user_id=1,
                administrator_id=1,
                co_administrator_ids=[],
                member_ids=[],
                name='Project 3',
                description='The third test project to be created',
                created_at=datetime.utcnow(),
            ),
            Project(
                project_id=4,
                user_id=2,
                administrator_id=2,
                co_administrator_ids=[],
                member_ids=[],
                name='Project 4',
                description='The fourth test project to be created',
                created_at=datetime.utcnow(),
            ),
            Project(
                project_id=5,
                user_id=2,
                administrator_id=2,
                co_administrator_ids=[],
                member_ids=[],
                name='Project 5',
                description='The fifth test project to be created',
                created_at=datetime.utcnow(),
            ),
            Project(
                project_id=6,
                user_id=2,
                administrator_id=2,
                co_administrator_ids=[],
                member_ids=[],
                name='Project 6',
                description='The sixth test project to be created',
                created_at=datetime.utcnow(),
            ),
        ]

    def initialize_database(self: 'ProjectTestDataLoader') -> None:
        projects: List[Project] = self.projects()

        for project in projects:
            project.create()


if __name__ == '__main__':
    ProjectTestDataLoader().initialize_database()
