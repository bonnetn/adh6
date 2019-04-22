# coding=utf-8
"""
Implements everything related to actions on the SQL database.
"""
from typing import List

from src.entity.room import Room
from src.use_case.interface.room_repository import RoomRepository


class RoomSQLStorage(RoomRepository):

    def search_room_by(self, ctx, owner_username=None) -> (List[Room], int):
        return [], 0
