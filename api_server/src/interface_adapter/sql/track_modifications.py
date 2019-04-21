# coding=utf-8
"""
Track modification on SQLAlchemy objects.
"""
from contextlib import contextmanager
from datetime import datetime

from src.constants import CTX_ADMIN
from src.interface_adapter.sql.model.models import Modification, Utilisateur
from src.interface_adapter.sql.model.trackable import RubyHashTrackable


@contextmanager
def track_modifications(ctx, session, obj: RubyHashTrackable):
    """
    Track the modifications of the specified entry and create a new entry in the modification table containing the diff.

    Object must inherit from RubyHashTrackable.
    """
    snap_before = obj.take_snapshot()  # Save the state of the object before actually modifying it.
    try:
        yield
    finally:
        diff = None

        if obj in session.new:
            diff = obj.serialize_snapshot_diff(None, obj.take_snapshot())

        elif obj in session.deleted:
            diff = obj.serialize_snapshot_diff(snap_before, None)

        elif snap_before != obj.take_snapshot():
            diff = obj.serialize_snapshot_diff(snap_before, obj.take_snapshot())

        if diff is None:
            return  # No modification.

        now = datetime.now()
        admin = ctx.get(CTX_ADMIN)
        member = obj.get_related_member()

        admin_id = session.query(Utilisateur).filter(Utilisateur.login == admin.login).one().id

        m = Modification(
            adherent_id=member.id,
            action=diff,
            created_at=now,
            updated_at=now,
            utilisateur_id=admin_id,
        )
        session.add(m)
