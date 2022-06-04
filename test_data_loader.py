from tests.user_test_data_loader import UserTestDataLoader
from tests.projects_test_data_loader import ProjectsTestDataLoader


UserTestDataLoader().initialize_database()
ProjectsTestDataLoader().initialize_database()
