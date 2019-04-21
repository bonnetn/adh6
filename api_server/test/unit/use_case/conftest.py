import datetime

from pytest import fixture

from src.entity.admin import Admin
from src.use_case.member_manager import MutationRequest
from src.util.context import build_context


@fixture
def ctx():
    return build_context(
        admin=Admin(login='test_admin'),
        testing=True,
    )


TEST_USERNAME = 'my_test_user'
TEST_EMAIL = 'hello@hello.fr'
TEST_FIRST_NAME = 'Jean'
TEST_LAST_NAME = 'Dupond'
TEST_COMMENT = 'This is a comment.'
TEST_ROOM_NUMBER = '1234'
TEST_DATE1 = datetime.datetime.fromisoformat('2019-04-21T11:11:46')
TEST_DATE2 = datetime.datetime.fromisoformat('2000-01-01T00:00:00')
TEST_LOGS = [
    'hello',
    'hi',
]
INVALID_MUTATION_REQ = [
    ('invalid_email', MutationRequest(email='not a valid email')),
    ('invalid_first_name', MutationRequest(first_name='')),
    ('invalid_last_name', MutationRequest(last_name='')),
    ('invalid_username', MutationRequest(username='')),
    ('invalid_room_number', MutationRequest(room_number='')),
]