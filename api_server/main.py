#!/usr/bin/env python3
import sys

import connexion
from connexion.resolver import RestyResolver

from config import CONFIGURATION, TEST_CONFIGURATION
from src.interface_adapter.elasticsearch.storage import ElasticSearchStorage
from src.interface_adapter.sql.device_storage import DeviceSQLStorage
from src.interface_adapter.sql.member_storage import MemberSQLStorage
from src.interface_adapter.sql.model.database import Database
from src.interface_adapter.sql.network_object_storage import NetworkObjectSQLStorage
from src.interface_adapter.sql.room_storage import RoomSQLStorage
from src.use_case.device_manager import DeviceManager
from src.use_case.member_manager import MemberManager
from src.use_case.port_manager import PortManager

# Global variables that you can use in the app.
configuration = None
member_sql_storage = None
port_sql_storage = None
device_sql_storage = None
room_sql_storage = None
elk_storage = None
port_manager = None
device_manager = None
member_manager = None
app = None


def init(m, testing=True):
    """
    Initialize and wire together the dependency of the application.
    """
    if testing:
        m.configuration = TEST_CONFIGURATION
    else:
        m.configuration = CONFIGURATION

    Database.init_db(m.configuration.DATABASE)

    m.member_sql_storage = MemberSQLStorage()
    m.network_object_sql_storage = NetworkObjectSQLStorage()
    m.device_sql_storage = DeviceSQLStorage()
    m.room_sql_storage = RoomSQLStorage()
    m.elk_storage = ElasticSearchStorage(m.configuration)

    m.port_manager = PortManager(
        port_storage=m.network_object_sql_storage,
    )
    m.device_manager = DeviceManager(
        device_storage=m.device_sql_storage,
        member_storage=m.member_sql_storage,
        room_storage=m.room_sql_storage,
        vlan_storage=m.network_object_sql_storage,
        ip_allocator=m.device_sql_storage,
    )
    m.member_manager = MemberManager(
        member_storage=m.member_sql_storage,
        membership_storage=m.member_sql_storage,
        logs_storage=m.elk_storage,
        configuration=m.configuration,
    )

    app = connexion.FlaskApp(__name__)
    app.app.config.update(m.configuration.API_CONF)
    app.add_api('swagger.yaml',
                resolver=RestyResolver('src.interface_adapter.http_api'),
                validate_responses=True,
                strict_validation=True,
                pythonic_params=True,
                )

    m.app = app


if __name__ == 'main' and not hasattr(sys, '_called_from_test'):
    init(sys.modules[__name__], testing=False)
    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    application = app.app
