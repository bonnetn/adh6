import logging

import sqlalchemy

from adh.constants import CTX_SQL_SESSION, CTX_ADMIN
from adh.interface_adapter.sql.model.models import Adherent, Chambre


class MemberManager:
    def search(self, ctx, limit, offset=0, room_number=None, terms=None):
        s = ctx.get(CTX_SQL_SESSION)
        if limit < 0:
            raise ValueError("limit must be positive")

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

        logging.info("%s fetched the member list", ctx.get(CTX_ADMIN))
        return list(map(dict, r)), count

    def add_new_member(self) -> None:
        return
