#!/usr/bin/env python3
import sys

import connexion

from config import CONFIGURATION, TEST_CONFIGURATION
from src.interface_adapter.elasticsearch.repository import ElasticSearchRepository
from src.interface_adapter.http_api.account import AccountHandler
from src.interface_adapter.http_api.account_type import AccountTypeHandler
from src.interface_adapter.http_api.device import DeviceHandler
from src.interface_adapter.http_api.member import MemberHandler
from src.interface_adapter.http_api.payment_method import PaymentMethodHandler
from src.interface_adapter.http_api.port import PortHandler
from src.interface_adapter.http_api.product import ProductHandler
from src.interface_adapter.http_api.room import RoomHandler
from src.interface_adapter.http_api.switch import SwitchHandler
from src.interface_adapter.http_api.temporary_account import TemporaryAccountHandler
from src.interface_adapter.http_api.transaction import TransactionHandler
from src.interface_adapter.sql.device_repository import DeviceSQLRepository
from src.interface_adapter.sql.member_repository import MemberSQLRepository
from src.interface_adapter.sql.model.database import Database
from src.interface_adapter.sql.money_repository import MoneySQLRepository
from src.interface_adapter.sql.network_object_repository import NetworkObjectSQLRepository
from src.interface_adapter.sql.room_repository import RoomSQLRepository
from src.resolver import MyResolver
from src.use_case.device_manager import DeviceManager
from src.use_case.member_manager import MemberManager
from src.use_case.port_manager import PortManager
from src.use_case.room_manager import RoomManager
from src.use_case.switch_manager import SwitchManager


def init(m, testing=True):
    """
    Initialize and wire together the dependency of the application.
    """
    if testing:
        configuration = TEST_CONFIGURATION
    else:
        configuration = CONFIGURATION

    Database.init_db(configuration.DATABASE)

    # Repositories:
    member_sql_repository = MemberSQLRepository()
    network_object_sql_repository = NetworkObjectSQLRepository()
    device_sql_repository = DeviceSQLRepository()
    room_sql_repository = RoomSQLRepository()
    elk_repository = ElasticSearchRepository(configuration)
    money_repository = MoneySQLRepository()

    # Managers
    switch_manager = SwitchManager(
        switch_repository=network_object_sql_repository,
    )
    port_manager = PortManager(
        port_repository=network_object_sql_repository,
    )
    device_manager = DeviceManager(
        device_repository=device_sql_repository,
        member_repository=member_sql_repository,
        room_repository=room_sql_repository,
        vlan_repository=network_object_sql_repository,
        ip_allocator=device_sql_repository,
    )
    member_manager = MemberManager(
        member_repository=member_sql_repository,
        money_repository=money_repository,
        membership_repository=member_sql_repository,
        logs_repository=elk_repository,
        configuration=configuration,
    )
    room_manager = RoomManager(
        room_repository=room_sql_repository,
    )

    # HTTP Handlers:
    transaction_handler = TransactionHandler()
    member_handler = MemberHandler(member_manager)
    device_handler = DeviceHandler(device_manager)
    room_handler = RoomHandler(room_manager)
    switch_handler = SwitchHandler(switch_manager)
    port_handler = PortHandler(port_manager)
    temporary_account_handler = TemporaryAccountHandler()
    account_type_handler = AccountTypeHandler()
    payment_method_handler = PaymentMethodHandler()
    account_handler = AccountHandler()
    product_handler = ProductHandler()

    app = connexion.FlaskApp(__name__, specification_dir='openapi', host='localhost', port=1234)
    app.app.config.update(configuration.API_CONF)

    app.add_api('swagger.yaml',
                # resolver=RestyResolver('src.interface_adapter.http_api'),
                resolver=MyResolver({
                    'transaction': transaction_handler,
                    'member': member_handler,
                    'device': device_handler,
                    'room': room_handler,
                    'switch': switch_handler,
                    'port': port_handler,
                    'temporary_account': temporary_account_handler,
                    'account_type': account_type_handler,
                    'payment_method': payment_method_handler,
                    'account': account_handler,
                    'product': product_handler,
                }),
                validate_responses=True,
                strict_validation=True,
                pythonic_params=True,
                )

    m.application = app


# When run with uWSGI (production).
if __name__ == 'uwsgi_file_main':
    init(sys.modules[__name__], testing=False)

# When run with `python main.py`, when people want to run it locally.
if __name__ == '__main__' and not hasattr(sys, '_called_from_test'):
    init(sys.modules[__name__], testing=False)
    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    application.run()
