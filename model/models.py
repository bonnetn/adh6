# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, \
        Numeric, String, Text, text, ForeignKey
from sqlalchemy.orm import relationship

from model.database import Base


class Adherent(Base):
    __tablename__ = 'adherents'

    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    prenom = Column(String(255))
    mail = Column(String(255))
    login = Column(String(255))
    password = Column(String(255))
    chambre_id = Column(Integer, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    date_de_depart = Column(Date)
    commentaires = Column(String(255))
    mode_association = Column(
        DateTime,
        server_default=text("'2011-04-30 17:50:17'")
    )
    access_token = Column(String(255))


class Caisse(Base):
    __tablename__ = 'caisse'

    id = Column(Integer, primary_key=True)
    fond = Column(Numeric(10, 2))
    coffre = Column(Numeric(10, 2))
    date = Column(DateTime)
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
    vlan_id = Column(Integer, index=True)


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
    adherent = relationship("Adherent")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_seen = Column(DateTime)
    ipv6 = Column(String(255))


class Portable(Base):
    __tablename__ = 'portables'

    id = Column(Integer, primary_key=True)
    mac = Column(String(255))
    adherent_id = Column(Integer, ForeignKey(Adherent.id), nullable=False)
    adherent = relationship("Adherent")
    last_seen = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Port(Base):
    __tablename__ = 'ports'

    id = Column(Integer, primary_key=True)
    rcom = Column(Integer)
    numero = Column(String(255))
    oid = Column(String(255))
    switch_id = Column(Integer, index=True)
    chambre_id = Column(Integer, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Switch(Base):
    __tablename__ = 'switches'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    ip = Column(String(255))
    communaute = Column(String(255))
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


class Vlan(Base):
    __tablename__ = 'vlans'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer)
    adresses = Column(String(255))
    adressesv6 = Column(String(255))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
