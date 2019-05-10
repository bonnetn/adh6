#!/usr/bin/env python3
import sys

import connexion
from connexion.resolver import RestyResolver

from config import CONFIGURATION, TEST_CONFIGURATION
from src.interface_adapter.elasticsearch.repository import ElasticSearchRepository
from src.interface_adapter.sql.device_repository import DeviceSQLRepository
from src.interface_adapter.sql.member_repository import MemberSQLRepository
from src.interface_adapter.sql.model.database import Database
from src.interface_adapter.sql.money_repository import MoneySQLRepository
from src.interface_adapter.sql.network_object_repository import NetworkObjectSQLRepository
from src.interface_adapter.sql.room_repository import RoomSQLRepository
from src.use_case.device_manager import DeviceManager
from src.use_case.interface.money_repository import MoneyRepository
from src.use_case.member_manager import MemberManager
from src.use_case.port_manager import PortManager
from src.use_case.room_manager import RoomManager
from src.use_case.switch_manager import SwitchManager

# Global variables that you can use in the app.
configuration = None

# Interface handlers.
member_sql_repository: MemberSQLRepository = None
port_sql_repository: NetworkObjectSQLRepository = None
device_sql_repository: DeviceSQLRepository = None
room_sql_repository: RoomSQLRepository = None
elk_repository: ElasticSearchRepository = None
money_repository: MoneyRepository = None

# Use cases.
port_manager: PortManager = None
device_manager: DeviceManager = None
member_manager: MemberManager = None
room_manager: RoomManager = None
switch_manager: SwitchManager = None

# Application.
application = None


def init(m, testing=True):
    """
    Initialize and wire together the dependency of the application.
    """
    if testing:
        m.configuration = TEST_CONFIGURATION
    else:
        m.configuration = CONFIGURATION

    Database.init_db(m.configuration.DATABASE)

    m.member_sql_repository = MemberSQLRepository()
    m.network_object_sql_repository = NetworkObjectSQLRepository()
    m.device_sql_repository = DeviceSQLRepository()
    m.room_sql_repository = RoomSQLRepository()
    m.elk_repository = ElasticSearchRepository(m.configuration)
    m.money_repository = MoneySQLRepository()

    m.switch_manager = SwitchManager(
        switch_repository=m.network_object_sql_repository,
    )
    m.port_manager = PortManager(
        port_repository=m.network_object_sql_repository,
    )
    m.device_manager = DeviceManager(
        device_repository=m.device_sql_repository,
        member_repository=m.member_sql_repository,
        room_repository=m.room_sql_repository,
        vlan_repository=m.network_object_sql_repository,
        ip_allocator=m.device_sql_repository,
    )
    m.member_manager = MemberManager(
        member_repository=m.member_sql_repository,
        money_repository=money_repository,
        membership_repository=m.member_sql_repository,
        logs_repository=m.elk_repository,
        configuration=m.configuration,
    )
    m.room_manager = RoomManager(
        room_repository=m.room_sql_repository,
    )

    app = connexion.FlaskApp(__name__, specification_dir='openapi', host='localhost', port=1234)
    app.app.config.update(m.configuration.API_CONF)
    app.add_api('swagger.yaml',
                resolver=RestyResolver('src.interface_adapter.http_api'),
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
