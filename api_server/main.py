#!/usr/bin/env python3
import connexion
from connexion.resolver import RestyResolver

from config import CONFIGURATION
from config.CONFIGURATION import API_CONF, PROD_DATABASE
from src.interface_adapter.elasticsearch.storage import ElasticSearchStorage
from src.interface_adapter.sql.device_storage import DeviceSQLStorage
from src.interface_adapter.sql.member_storage import MemberSQLStorage
from src.interface_adapter.sql.model.database import Database
from src.interface_adapter.sql.port_storage import PortSQLStorage
from src.interface_adapter.sql.room_storage import RoomSQLStorage
from src.use_case.device_manager import DeviceManager
from src.use_case.member_manager import MemberManager
from src.use_case.port_manager import PortManager

Database.init_db(PROD_DATABASE)

member_sql_storage = MemberSQLStorage()
port_sql_storage = PortSQLStorage()
device_sql_storage = DeviceSQLStorage()
room_sql_storage = RoomSQLStorage()
elk_storage = ElasticSearchStorage(CONFIGURATION)

port_manager = PortManager(
    port_storage=port_sql_storage,
)
device_manager = DeviceManager(
    device_storage=device_sql_storage,
    member_storage=member_sql_storage,
    room_storage=room_sql_storage,
    ip_allocator=device_sql_storage,
)
member_manager = MemberManager(
    member_storage=member_sql_storage,
    membership_storage=member_sql_storage,
    logs_storage=elk_storage,
    configuration=CONFIGURATION,
)

app = connexion.FlaskApp(__name__)
app.app.config.update(API_CONF)
app.add_api('swagger.yaml',
            resolver=RestyResolver('src.interface_adapter.http_api'),
            validate_responses=True,
            strict_validation=True,
            pythonic_params=True,
            )
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app
