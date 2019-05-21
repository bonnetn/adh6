# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, String, TIMESTAMP, TEXT, Boolean
from sqlalchemy import Date, DateTime, Integer, \
    Numeric, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.interface_adapter.sql.model.trackable import RubyHashTrackable
from src.interface_adapter.sql.util.rubydiff import rubydiff

Base = declarative_base()


class Vlan(Base):
    __tablename__ = 'vlans'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer)
    adresses = Column(String(255))
    adressesv6 = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Chambre(Base):
    __tablename__ = 'chambres'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer)
    description = Column(String(255))
    telephone = Column(String(255))
    vlan_old = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    dernier_adherent = Column(Integer)
    vlan_id = Column(Integer, ForeignKey(Vlan.id))
    vlan = relationship(Vlan)


class Adherent(Base, RubyHashTrackable):
    __tablename__ = 'adherents'

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    mail = Column(String(255))
    login = Column(String(255))
    password = Column(String(255))
    chambre_id = Column(Integer, ForeignKey(Chambre.id))
    chambre = relationship(Chambre)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    date_de_depart = Column(Date)
    commentaires = Column(String(255))
    mode_association = Column(
        DateTime,
        server_default=text("'2011-04-30 17:50:17'")
    )
    access_token = Column(String(255))

    def take_snapshot(self) -> dict:
        snap = super().take_snapshot()
        if 'password' in snap:
            del snap['password']  # Let's not track the password changes, this is none of our business. :)
        return snap

    def serialize_snapshot_diff(self, snap_before: dict, snap_after: dict) -> str:
        """
        Override this method to add the prefix.
        """

        modif = rubydiff(snap_before, snap_after)
        modif = '--- !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n' + modif
        return modif

    def get_related_member(self):
        return self


class Caisse(Base):
    __tablename__ = 'caisse'

    id = Column(Integer, primary_key=True)
    fond = Column(Numeric(10, 2))
    coffre = Column(Numeric(10, 2))
    date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Compte(Base):
    __tablename__ = 'comptes'

    id = Column(Integer, primary_key=True)
    intitule = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Inscription(Base):
    __tablename__ = 'inscriptions'

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    email = Column(String(255))
    login = Column(String(255))
    password = Column(String(255))
    chambre_id = Column(Integer, index=True)
    duree_cotisation = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class MacVendor(Base):
    __tablename__ = 'mac_vendors'

    id = Column(Integer, primary_key=True)
    prefix = Column(String(255))
    nom = Column(String(255))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Modification(Base):
    __tablename__ = 'modifications'

    id = Column(Integer, primary_key=True)
    adherent_id = Column(Integer, index=True)
    action = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    utilisateur_id = Column(Integer, index=True)


class Ordinateur(Base, RubyHashTrackable):
    __tablename__ = 'ordinateurs'

    id = Column(Integer, primary_key=True)
    mac = Column(String(255))
    ip = Column(String(255))
    dns = Column(String(255))
    adherent_id = Column(Integer, ForeignKey(Adherent.id), nullable=False)
    adherent = relationship(Adherent)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_seen = Column(DateTime)
    ipv6 = Column(String(255))

    def serialize_snapshot_diff(self, snap_before: dict, snap_after: dict) -> str:
        """
        Override this method to add the prefix.
        """
        modif = rubydiff(snap_before, snap_after)
        if snap_after is None:
            proper_mac = snap_before.get('mac').upper().replace(":", "-")
            return (
                "---\n"
                "ordinateur: Suppression de l'ordinateur {}\n".format(proper_mac)
            )

        modif = 'ordinateur: !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n' + modif
        return modif

    def get_related_member(self):
        return self.adherent


class Portable(Base, RubyHashTrackable):
    __tablename__ = 'portables'

    id = Column(Integer, primary_key=True)
    mac = Column(String(255))
    adherent_id = Column(Integer, ForeignKey(Adherent.id), nullable=False)
    adherent = relationship(Adherent)
    last_seen = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def serialize_snapshot_diff(self, snap_before: dict, snap_after: dict) -> str:
        """
        Override this method to add the prefix.
        """
        modif = rubydiff(snap_before, snap_after)
        if snap_after is None:
            proper_mac = snap_before.get('mac').upper().replace(":", "-")
            return (
                "---\n"
                "portable: Suppression du portable {}\n".format(proper_mac)
            )
        modif = 'portable: !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n' + modif
        return modif

    def get_related_member(self):
        return self.adherent


class Switch(Base):
    __tablename__ = 'switches'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    ip = Column(String(255))
    communaute = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Port(Base):
    __tablename__ = 'ports'

    id = Column(Integer, primary_key=True)
    rcom = Column(Integer)
    numero = Column(String(255))
    oid = Column(String(255))
    switch_id = Column(Integer, ForeignKey(Switch.id), nullable=False)
    switch = relationship(Switch)
    chambre_id = Column(Integer, ForeignKey(Chambre.id), nullable=False)
    chambre = relationship(Chambre)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Utilisateur(Base):
    __tablename__ = 'utilisateurs'

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    access = Column(Integer)
    email = Column(String(255))
    login = Column(String(255))
    password_hash = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    access_token = Column(String(255))


class Adhesion(Base):
    __tablename__ = 'adhesion'

    id = Column(Integer, primary_key=True)
    adherent_id = Column(Integer, ForeignKey(Adherent.id), nullable=False)
    adherent = relationship(Adherent)
    depart = Column(DateTime, nullable=False)
    fin = Column(DateTime, nullable=False)


class NainA(Base):
    __tablename__ = 'temporary_account'

    id = Column(Integer, primary_key=True)

    # Name of the 1A.
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    # Access token that she/he will use.
    access_token = Column(Text, nullable=False)
    # Time window when she/he will have access to ADH database.
    start_time = Column(DateTime, nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    # Administrator who created that temporary account.
    admin = Column(Text, nullable=False)


class AccountType(Base):
    __tablename__ = 'account_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class PaymentMethod(Base):
    __tablename__ = 'payment_method'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    buying_price = Column(DECIMAL(8, 2), nullable=False)
    selling_price = Column(DECIMAL(8, 2), nullable=False)
    name = Column(String(255), nullable=False)


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, unique=True)
    type = Column(ForeignKey('account_type.id'), nullable=False, index=True)
    creation_date = Column(TIMESTAMP, nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    actif = Column(Boolean(), nullable=False)

    account_type = relationship('AccountType')


class Transaction(Base, RubyHashTrackable):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    value = Column(DECIMAL(8, 2), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    src = Column(ForeignKey('account.id'), nullable=False, index=True)
    dst = Column(ForeignKey('account.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    attachments = Column(TEXT(65535), nullable=False)
    type = Column(ForeignKey('payment_method.id'), nullable=False, index=True)

    dst_account = relationship('Account', foreign_keys=[dst])
    src_account = relationship('Account', foreign_keys=[src])
    payment_method = relationship('PaymentMethod')

    def serialize_snapshot_diff(self, snap_before: dict, snap_after: dict) -> str:
        """
        Override this method to add the prefix.
        """

        modif = rubydiff(snap_before, snap_after)
        modif = '--- !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n' + modif
        return modif

    def get_related_member(self):
        return self


class Ecriture(Base):
    __tablename__ = 'ecritures'

    id = Column(Integer, primary_key=True)
    intitule = Column(String(255))
    montant = Column(Numeric(10, 2))
    moyen = Column(String(255))
    date = Column(DateTime)
    compte_id = Column(Integer, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    utilisateur_id = Column(Integer, ForeignKey(Utilisateur.id), index=True)
    utilisateur = relationship(Utilisateur)
    adherent_id = Column(Integer, ForeignKey(Adherent.id), index=True)
    adherent = relationship(Adherent)
