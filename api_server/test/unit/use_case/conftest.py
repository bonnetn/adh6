import datetime
from pytest import fixture

from src.entity.admin import Admin
from src.entity.device import Device, DeviceType
from src.entity.member import Member
from src.entity.room import Room, Vlan
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
TEST_MAC_ADDRESS1 = 'A0-B1-5A-C1-5F-E3'
TEST_MAC_ADDRESS2 = '10-0E-9C-19-FF-64'
INVALID_MUTATION_REQ = [
    ('invalid_email', MutationRequest(email='not a valid email')),
    ('invalid_first_name', MutationRequest(first_name='')),
    ('invalid_last_name', MutationRequest(last_name='')),
    ('invalid_username', MutationRequest(username='')),
    ('invalid_room_number', MutationRequest(room_number='')),
]


@fixture
def sample_member():
    return Member(
        username=TEST_USERNAME,
        email=TEST_EMAIL,
        first_name=TEST_FIRST_NAME,
        last_name=TEST_LAST_NAME,
        departure_date=TEST_DATE1.isoformat(),
        comment=TEST_COMMENT,
        association_mode=TEST_DATE2.isoformat(),
        room_number=str(TEST_ROOM_NUMBER),
    )


@fixture
def sample_device():
    return Device(
        mac_address='FF-FF-FF-FF-FF-FF',
        owner_username=TEST_USERNAME,
        connection_type=DeviceType.Wired,
        ip_v4_address='127.0.0.1',
        ip_v6_address='127.0.0.1',
    )


@fixture
def sample_room():
    return Room(
        room_number='1234',
        description='Test room.',
        vlan=Vlan(
            number='42',
            ip_v4_range='192.0.0.0/24',
            ip_v6_range='fe80::/10',
        ),
        phone_number=None,
    )
