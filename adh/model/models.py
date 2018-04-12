# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, \
        Numeric, String, Text, text, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.orm.exc import NoResultFound
from adh.util import checks
from adh.model.database import Base
from adh.exceptions import InvalidIPv4, InvalidIPv6, InvalidEmail, InvalidMac
from adh.exceptions import UserNotFound, RoomNotFound
from adh.util.date import string_to_date


class Vlan(Base):
    __tablename__ = 'vlans'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer)
    adresses = Column(String(255))
    adressesv6 = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

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


class Adherent(Base):
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

    @staticmethod
    def find(session, username):
        if not username:
            return None
        q = session.query(Adherent)
        q = q.filter(Adherent.login == username)
        try:
            return q.one()
        except NoResultFound:
            raise UserNotFound()

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
        if not mail or not checks.isEmail(mail):
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


class Ordinateur(Base):
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

    @validates('mac')
    def mac_valid(self, key, mac):
        if not mac or not checks.isMac(mac):
            raise InvalidMac()
        return mac

    @validates('ip')
    def valid_ip(self, key, addr):
        if not addr or not checks.isIPv4(addr):
            raise InvalidIPv4()
        return addr

    @validates('ipv6')
    def valid_ipv6(self, key, addr):
        if not addr or not checks.isIPv6(addr):
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


class Portable(Base):
    __tablename__ = 'portables'

    id = Column(Integer, primary_key=True)
    mac = Column(String(255))
    adherent_id = Column(Integer, ForeignKey(Adherent.id), nullable=False)
    adherent = relationship(Adherent)
    last_seen = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    @validates('mac')
    def mac_valid(self, key, mac):
        if not mac or not checks.isMac(mac):
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
    def from_dict(body):
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


class Adhesion(Base):
    __tablename__ = 'adhesion'

    id = Column(Integer, primary_key=True)
    adherent_id = Column(Integer, ForeignKey(Adherent.id), nullable=False)
    adherent = relationship(Adherent)
    depart = Column(DateTime, nullable=False)
    fin = Column(DateTime, nullable=False)
