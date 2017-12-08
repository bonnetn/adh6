from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
 
 
Base = declarative_base()

class User(Base):
    __tablename__ = "adherents"
    id = Column(Integer, primary_key=True)
    nom = Column(String, Nullable=False)
    prenom = Column(String, Nullable=False)
    mail = Column(String, Nullable=False)
    login = Column(String, Nullable=False, unique=True)
    password = Column(String, Nullable=False)
    chambre_id = Column(Integer, ForeignKey('chambres.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    date_de_depart = Column(DateTime)
    commentaires = Column(String)
    mode_association = Column(DateTime)
    access_token = Column(String)

class Room(Base):
    __tablename__ = "chambres"
    id = Column(Integer, primary_key=True)
    numero = Column(Integer, unique=True)
    description = Column(String)
    telephone = Column(String)
    vlan_old = Column(Integer)
    vlan_id = Column(Integer, ForeignKey('vlans.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    dernier_adherent = Column(Integer)

class Vlan(Base):
    __tablename__ = "vlans"
    id = Column(Integer, primary_key=True)
    numero = Column(Integer)
    adresses = Column(String)
    adressesv6 = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class WiredDevice(Base):
    __tablename__ = "ordinateurs"
    id = Column(Integer, primary_key=True)
    mac = Column(String, Nullable=False, unique=True)
    ip = Column(String)
    dns = Column(String)
    adherent_id = Column(Integer, ForeignKey('adherents.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_seen =  Column(DateTime)
    ipv6 = Column(String)

class WirelessDevice(Base):
    __tablename__ = "portables"
    id = Column(Integer, primary_key=True)
    mac = Column(String, Nullable=False, unique=True)
    adherent_id = Column(Integer, ForeignKey('adherents.id'))
    last_seen = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Port(Base):
    __tablename__ = "ports"
    id = Column(Integer, primary_key=True)
    rcom = Column(Integer)
    numero = Column(String)
    oid = Column(String)
    switch_id = Column(Integer, ForeignKey('switches.id'))
    chambre_id = Column(Integer, ForeignKey('chambres.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Switch(Base):
    __tablename__ = "switches"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    ip = Column(String)
    communaute = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
 
from sqlalchemy import create_engine
engine = create_engine('mysql://adh:tototo@localhost/foo') 

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
