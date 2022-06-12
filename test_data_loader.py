from tests.user_test_data_loader import UserTestDataLoader
from tests.project_test_data_loader import ProjectTestDataLoader
from tests.column_test_data_loader import ColumnTestDataLoader

UserTestDataLoader().initialize_database()
ProjectTestDataLoader().initialize_database()
ColumnTestDataLoader().initialize_database()
