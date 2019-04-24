# coding: utf-8
import datetime

from sqlalchemy import Column, DECIMAL, ForeignKey, String, TIMESTAMP, TEXT
from sqlalchemy import Date, DateTime, Integer, \
    Numeric, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.orm.exc import NoResultFound

from src.exceptions import InvalidIPv4, InvalidIPv6, InvalidEmail, InvalidMac
from src.exceptions import RoomNotFound, SwitchNotFound
from src.exceptions import VlanNotFound, PortNotFound
from src.interface_adapter.sql.model.trackable import RubyHashTrackable
from src.interface_adapter.sql.util.rubydiff import rubydiff
from src.use_case.member_manager import MemberNotFound
from src.util import checks
from src.util.date import string_to_date

Base = declarative_base()


class Vlan(Base):
    __tablename__ = 'vlans'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer)
    adresses = Column(String(255))
    adressesv6 = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    @staticmethod
    def find(session, num):
        """ [API] Get the specified Vlan from the database """
        try:
            q = session.query(Vlan)
            q = q.filter(Vlan.numero == num)
            return q.one()
        except NoResultFound:
            raise VlanNotFound

    @validates('adresses')
    def valid_ipv4(self, key, addr):
        if not checks.isIPv4Network(addr):
            raise InvalidIPv4()
        return addr

    @validates('adressesv6')
    def valid_ipv6(self, key, addr):
        if not checks.isIPv6Network(addr):
            raise InvalidIPv4()
        return addr


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

    @staticmethod
    def from_dict(session, d):
        return Chambre(
            numero=d.get("roomNumber"),
            description=d.get("description"),
            telephone=d.get("phone"),
            vlan=Vlan.find(session, d.get("vlan")),
        )

    @staticmethod
    def find(session, roomNumber):
        if not roomNumber:
            return None
        q = session.query(Chambre)
        q = q.filter(Chambre.numero == roomNumber)
        try:
            return q.one()
        except NoResultFound:
            raise RoomNotFound()

    @validates('numero')
    def not_empty(self, key, s):
        if not s:
            raise ValueError("String must not be empty")
        return s

    def __iter__(self):
        yield "roomNumber", self.numero
        if self.description:
            yield "description", self.description
        if self.telephone:
            yield "phone", self.telephone
        if self.vlan:
            yield "vlan", self.vlan.numero


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

    @staticmethod
    def find(session, username):
        if not username:
            return None
        q = session.query(Adherent)
        q = q.filter(Adherent.login == username)
        try:
            return q.one()
        except NoResultFound:
            raise MemberNotFound()

    @staticmethod
    def from_dict(session, d):
        return Adherent(
            mail=d.get("email"),
            prenom=d.get("firstName"),
            nom=d.get("lastName"),
            login=d.get("username"),
            date_de_depart=string_to_date(d.get('departureDate')),
            commentaires=d.get('comment'),
            mode_association=string_to_date(d.get('associationMode')),
            chambre=Chambre.find(session, d.get("roomNumber")),
        )

    @validates('nom', 'prenom', 'login', 'password')
    def not_empty(self, key, s):
        if not s:
            raise ValueError("String must not be empty")
        return s

    @validates('mail')
    def valid_email(self, key, mail):
        if not mail or not checks.is_email(mail):
            raise InvalidEmail()
        return mail

    def __iter__(self):
        yield "email", self.mail
        yield "firstName", self.prenom
        yield "lastName", self.nom
        yield "username", self.login
        if self.commentaires:
            yield "comment", self.commentaires

        if self.chambre:
            yield "roomNumber", self.chambre.numero

        if self.date_de_depart:
            yield "departureDate", self.date_de_depart

        if self.mode_association:
            yield "associationMode", self.mode_association


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
    utilisateur_id = Column(Integer, index=True)
    adherent_id = Column(Integer, index=True)


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

    @staticmethod
    def add(session, object_updated, admin):
        now = datetime.datetime.now()
        # action, adherent = object_updated.get_ruby_modif()
        m = Modification(
            adherent_id=adherent.id,
            action=action,
            created_at=now,
            updated_at=now,
            utilisateur_id=admin.id
        )
        session.add(m)


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

    @validates('mac')
    def mac_valid(self, key, mac):
        if not mac or not checks.is_mac_address(mac):
            raise InvalidMac(mac)
        return mac

    @validates('ip')
    def valid_ip(self, key, addr):
        if not addr or (not checks.isIPv4(addr) and addr != "En Attente"):
            raise InvalidIPv4(addr)
        return addr

    @validates('ipv6')
    def valid_ipv6(self, key, addr):
        if not addr or (not checks.isIPv6(addr) and addr != "En Attente"):
            raise InvalidIPv6()
        return addr

    def __iter__(self):
        yield "mac", self.mac
        yield "connectionType", "wired"
        if self.ip:
            yield "ipAddress", self.ip
        if self.ipv6:
            yield "ipv6Address", self.ipv6
        if self.adherent:
            yield "username", self.adherent.login


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

    @validates('mac')
    def mac_valid(self, key, mac):
        if not mac or not checks.is_mac_address(mac):
            raise InvalidMac()
        return mac

    def __iter__(self):
        yield "mac", self.mac
        yield "connectionType", "wireless"
        if self.adherent:
            yield "username", self.adherent.login


class Switch(Base):
    __tablename__ = 'switches'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    ip = Column(String(255))
    communaute = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    @staticmethod
    def find(session, switchID):
        """ [API] Get the specified switch from the database """
        try:
            q = session.query(Switch)
            q = q.filter(Switch.id == switchID)
            return q.one()
        except NoResultFound:
            raise SwitchNotFound

    @staticmethod
    def from_dict(session, body):
        """ Transforms a dictionary to Switch object """
        return Switch(
            description=body.get('description'),
            ip=body.get('ip'),
            communaute=body.get('community'),
        )

    @validates('ip')
    def valid_ip(self, key, addr):
        if not addr or not checks.isIPv4(addr):
            raise InvalidIPv4()
        return addr

    def __iter__(self):
        yield "id", self.id
        yield "ip", self.ip
        yield "community", self.communaute
        if self.description:
            yield "description", self.description


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

    @staticmethod
    def find(session, port_id):
        """ [API] Get the specified Port from the database """
        try:
            q = session.query(Port)
            q = q.filter(Port.id == port_id)
            return q.one()
        except NoResultFound:
            raise PortNotFound

    @staticmethod
    def from_dict(session, d):
        """ Creates a Port object from a request """
        return Port(
            chambre=Chambre.find(session, d.get("roomNumber")),
            switch=Switch.find(session, d.get("switchID")),
            numero=d.get("portNumber"),
        )

    @validates('numero')
    def not_empty(self, key, s):
        if not s:
            raise ValueError("String must not be empty")
        return s

    def __iter__(self):
        yield "id", self.id
        yield "portNumber", self.numero
        if self.chambre:
            yield "roomNumber", self.chambre.numero
        if self.switch_id:
            yield "switchID", self.switch_id


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

    @staticmethod
    def find_or_create(session, username):
        """ Get the specified admin, if it does not exist, create it. """
        try:
            q = session.query(Utilisateur)
            q = q.filter(Utilisateur.login == username)
            return q.one()
        except NoResultFound:
            now = datetime.datetime.now()
            new_admin = Utilisateur(
                nom="-",
                access=42,
                email="-",
                login=username,
                password_hash="-",
                created_at=now,
                updated_at=now,
                access_token="-"
            )
            session.add(new_admin)
            return new_admin


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

    account_type = relationship('AccountType')


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    product = Column(ForeignKey('product.id'), nullable=False, index=True)
    value = Column(DECIMAL(8, 2), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    src = Column(ForeignKey('account.id'), nullable=False, index=True)
    dst = Column(ForeignKey('account.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    attachments = Column(TEXT(65535), nullable=False)
    type = Column(ForeignKey('payment_method.id'), nullable=False, index=True)

    account = relationship('Account', primaryjoin='Transaction.dst == Account.id')
    product1 = relationship('Product')
    account1 = relationship('Account', primaryjoin='Transaction.src == Account.id')
    payment_method = relationship('PaymentMethod')
