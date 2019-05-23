import datetime

from pytest import fixture

from src.entity.admin import Admin
from src.entity.device import Device, DeviceType
from src.entity.member import Member
from src.entity.payment_method import PaymentMethod
from src.entity.port import Port, SwitchInfo
from src.entity.room import Room
from src.entity.switch import Switch
from src.entity.transaction import Transaction
from src.entity.account import Account
from src.entity.account_type import AccountType
from src.use_case.member_manager import FullMutationRequest
from src.util.context import build_context


@fixture
def ctx():
    return build_context(
        admin=Admin(login='test_admin'),
        testing=True,
    )


TEST_USERNAME = 'test_usr'
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
        vlan_number='42',
        phone_number=None,
    )


@fixture
def sample_port():
    return Port(
        id="1",
        port_number="test number",
        room_number="1234",
        switch_info=SwitchInfo(
            switch_id="1",
            rcom=42,
            oid="1.2.3"
        ),
    )


@fixture
def sample_switch():
    return Switch(
        id='1',
        ip_v4='127.0.0.1',
        description='description',
        community='community',
    )


@fixture
def sample_payment_method():
    return PaymentMethod(
        payment_method_id=0,
        name='liquide'
    )


@fixture
def sample_transaction():
    return Transaction(
        src='1',
        dst='2',
        name='description',
        value='200',
        attachments='',
        timestamp='',
        payment_method=PaymentMethod(
            payment_method_id=0,
            name='liquide'
        ))

@fixture
def sample_account():
    return Account(
        name='MiNET',
        type=AccountType.Club,
        actif=True,
        creation_date='21/05/2019',
    )
