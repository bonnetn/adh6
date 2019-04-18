from contextlib import contextmanager
from datetime import datetime

from adh.constants import CTX_ADMIN
from adh.interface_adapter.sql.model.models import Modification
from adh.interface_adapter.sql.model.trackable import RubyHashTrackable


@contextmanager
def track_modifications(ctx, session, obj: RubyHashTrackable):
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

        m = Modification(
            adherent_id=member.id,
            action=diff,
            created_at=now,
            updated_at=now,
            utilisateur_id=admin.id
        )
        session.add(m)
