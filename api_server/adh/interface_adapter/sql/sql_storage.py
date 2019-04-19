from datetime import datetime

import sqlalchemy

from adh.constants import CTX_SQL_SESSION
from adh.exceptions import MemberNotFound
from adh.interface_adapter.sql.model.models import Adherent, Chambre, Adhesion
from adh.interface_adapter.sql.track_modifications import track_modifications
from adh.use_case.interface.member_repository import MemberRepository
from adh.use_case.interface.membership_repository import MembershipRepository


class NotFoundError(ValueError):
    pass


class SQLStorage(MemberRepository, MembershipRepository):
    def add_membership(self, ctx, username, start, end):
        s = ctx.get(CTX_SQL_SESSION)

        member = _get_member_by_login(s, username)
        if member is None:
            raise NotFoundError('cannot find any member with that username')

        s.add(Adhesion(
            adherent=member,
            depart=start,
            fin=end
        ))

    def create_member(self, ctx,
                      last_name=None, first_name=None, email=None, username=None, comment=None,
                      room_number=None, departure_date=None, association_mode=None
                      ) -> None:
        s = ctx.get(CTX_SQL_SESSION)
        now = datetime.now()

        room = None
        if room_number is not None:
            room = s.query(Chambre).filter(Chambre.numero == room_number).one_or_none()
            if not room:
                raise ValueError('room not found')

        member = Adherent(
            nom=last_name,
            prenom=first_name,
            mail=email,
            login=username,
            chambre=room,
            created_at=now,
            updated_at=now,
            commentaires=comment,
            date_de_depart=departure_date,
            mode_association=association_mode,
        )

        with track_modifications(ctx, s, member):
            s.add(member)

    def update_member(self, ctx, member_to_update,
                      last_name=None, first_name=None, email=None, username=None, comment=None,
                      room_number=None, departure_date=None, association_mode=None, password=None
                      ) -> None:
        s = ctx.get(CTX_SQL_SESSION)

        member = _get_member_by_login(s, member_to_update)
        if member is None:
            raise MemberNotFound()

        with track_modifications(ctx, s, member):
            member.nom = last_name or member.nom
            member.prenom = first_name or member.prenom
            member.mail = email or member.mail
            member.commentaires = comment or member.commentaires
            member.login = username or member.login

            if departure_date is not None:
                member.date_de_depart = departure_date

            if association_mode is not None:
                member.mode_association = association_mode

            if room_number is not None:
                member.chambre = Chambre.find(s, room_number)

            member.updated_at = datetime.now()

        member.password = password or member.password  # Will not be tracked.

    def delete_member(self, ctx, username=None) -> None:
        s = ctx.get(CTX_SQL_SESSION)

        # Find the soon-to-be deleted user
        member = _get_member_by_login(s, username)
        if not member:
            raise ValueError(f"could not find user '{username}'")

        with track_modifications(ctx, s, member):
            # Actually delete it
            s.delete(member)

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


def _get_member_by_login(s, login) -> Adherent:
    return s.query(Adherent).filter(Adherent.login == login).one_or_none()
