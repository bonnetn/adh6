import sqlalchemy

from adh.constants import CTX_SQL_SESSION
from adh.interface_adapter.sql.model.models import Adherent, Chambre
from adh.interface_adapter.sql.track_modifications import track_modifications
from adh.use_case.interface.member_repository import MemberRepository
from adh.util.date import string_to_date


class SQLStorage(MemberRepository):
    def update_partially_member(self, ctx, member_to_update, **fields_to_update) -> None:
        fields_to_update = {k: v for k, v in fields_to_update.items() if v is not None}  # Remove the Nones in dict.

        s = ctx.get(CTX_SQL_SESSION)
        member = _get_member_by_login(s, member_to_update)

        with track_modifications(ctx, s, member):
            member.nom = fields_to_update.get("last_name", member.nom)
            member.prenom = fields_to_update.get("first_name", member.prenom)
            member.mail = fields_to_update.get("email", member.mail)
            member.commentaires = fields_to_update.get("comment", member.commentaires)
            member.login = fields_to_update.get("username", member.login)

            if "departure_date" in fields_to_update:
                member.date_de_depart = string_to_date(fields_to_update["departure_date"])

            if "association_mode" in fields_to_update:
                member.mode_association = string_to_date(fields_to_update["association_mode"])

            if "room_number" in fields_to_update:
                member.chambre = Chambre.find(s, fields_to_update["room_number"])

    def delete_member(self, ctx, username=None) -> None:
        s = ctx.get(CTX_SQL_SESSION)

        # Find the soon-to-be deleted user
        member = _get_member_by_login(s, username)
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


def _get_member_by_login(s, login):
    return s.query(Adherent).filter(Adherent.login == login).one_or_none()
