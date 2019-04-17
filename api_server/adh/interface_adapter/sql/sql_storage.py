import sqlalchemy

from adh.constants import CTX_SQL_SESSION
from adh.interface_adapter.sql.model.models import Adherent, Chambre
from adh.use_case.interface.member_repository import MemberRepository


class SQLStorage(MemberRepository):
    def search_member_by(self, ctx, limit=None, offset=None, room_number=None, terms=None) -> (list, int):
        s = ctx.get(CTX_SQL_SESSION)
        q = s.query(Adherent)
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
