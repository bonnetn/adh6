import sqlalchemy

from adh.constants import CTX_SQL_SESSION
from adh.interface_adapter.sql.model.models import Adherent, Chambre
from adh.interface_adapter.sql.track_modifications import track_modifications
from adh.use_case.interface.member_repository import MemberRepository


class SQLStorage(MemberRepository):
    def delete_member(self, ctx, username=None) -> None:
        s = ctx.get(CTX_SQL_SESSION)

        # Find the soon-to-be deleted user
        member = s.query(Adherent).filter(Adherent.login == username).one_or_none()
        if not member:
            raise ValueError(f"could not find user '{username}'")

        with track_modifications(ctx, s, member):
            # Actually delete it
            s.delete(member)

        # Write it in the modification table
        # Modification.add(s, member, ctx.get(CTX_ADMIN).admin)

    def search_member_by(self, ctx, limit=None, offset=None, room_number=None, terms=None, username=None) -> (
            list, int):
        s = ctx.get(CTX_SQL_SESSION)
        q = s.query(Adherent)

        if username:
            q = q.filter(Adherent.login == username)

        if room_number:
            try:
                q2 = s.query(Chambre)
                q2 = q2.filter(Chambre.numero == room_number)
                result = q2.one()
            except sqlalchemy.orm.exc.NoResultFound:
                return [], 0

            q = q.filter(Adherent.chambre == result)

        if terms:
            q = q.filter(
                (Adherent.nom.contains(terms)) |
                (Adherent.prenom.contains(terms)) |
                (Adherent.mail.contains(terms)) |
                (Adherent.login.contains(terms)) |
                (Adherent.commentaires.contains(terms))
            )

        count = q.count()
        q = q.order_by(Adherent.login.asc())
        q = q.offset(offset)
        q = q.limit(limit)
        r = q.all()

        return list(map(dict, r)), count
