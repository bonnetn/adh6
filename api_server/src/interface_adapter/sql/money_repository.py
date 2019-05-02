from datetime import datetime

from src.constants import CTX_SQL_SESSION, CTX_ADMIN
from src.exceptions import InvalidAdmin, UnknownPaymentMethod, MemberNotFound
from src.interface_adapter.sql.model.models import Ecriture, Utilisateur, Adherent
from src.use_case.interface.money_repository import MoneyRepository
from src.util.context import log_extra
from src.util.log import LOG

PAYMENT_METHOD_TO_DB = {
    'card': 'CB',
    'cash': 'Liquide',
    'bank_cheque': 'Chèque',
}


class MoneySQLRepository(MoneyRepository):
    def add_member_payment_record(self, ctx, amount_in_cents: int, title: str, member_username: str,
                                  payment_method: str) -> None:
        LOG.debug("sql_money_repository_add_payment_record",
                  extra=log_extra(ctx, amount=amount_in_cents / 100, title=title, username=member_username,
                                  payment_method=payment_method))
        now = datetime.now()
        s = ctx.get(CTX_SQL_SESSION)
        admin = ctx.get(CTX_ADMIN)

        admin_sql = s.query(Utilisateur).filter(Utilisateur.login == admin.login).one_or_none()
        if admin_sql is None:
            raise InvalidAdmin()

        member_sql = s.query(Adherent).filter(Adherent.login == member_username).one_or_none()
        if member_sql is None:
            raise MemberNotFound()

        payment_method_db = PAYMENT_METHOD_TO_DB.get(payment_method)
        if payment_method_db is None:
            raise UnknownPaymentMethod()

        e = Ecriture(
            intitule=title,
            montant=amount_in_cents / 100,
            moyen=payment_method,
            date=now,
            compte_id=1,  # Compte pour les paiement des adherents.
            created_at=now,
            updated_at=now,
            utilisateur=admin_sql,
            adherent=member_sql,
        )
        s.add(e)
