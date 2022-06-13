from datetime import datetime
from typing import List

from models import Column
from scripts.create_columns_table import default_raw_columns_data


class ColumnTestDataLoader:
    def __init__(self: 'ColumnTestDataLoader') -> None:
        pass

    def projects(self: 'ColumnTestDataLoader') -> List[Column]:
        return [
            Column(
                column_id=1,
                project_id=1,
                raw_columns=default_raw_columns_data(),
                created_at=datetime.utcnow(),
            ),
            Column(
                column_id=2,
                project_id=2,
                raw_columns=default_raw_columns_data(),
                created_at=datetime.utcnow(),
            ),
            Column(
                column_id=3,
                project_id=3,
                raw_columns=default_raw_columns_data(),
                created_at=datetime.utcnow(),
            ),
        ]

    def initialize_database(self: 'ColumnTestDataLoader') -> None:
        columns: List[Column] = self.projects()

        for column in columns:
            column.create()


if __name__ == '__main__':
    ColumnTestDataLoader().initialize_database()
