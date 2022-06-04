from tests.user_test_data_loader import UserTestDataLoader
from tests.project_test_data_loader import ProjectTestDataLoader


UserTestDataLoader().initialize_database()
ProjectTestDataLoader().initialize_database()
