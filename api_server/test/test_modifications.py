import pytest
from adh.model.database import Database as db
from CONFIGURATION import TEST_DATABASE as db_settings
from adh.model.models import (
    Adherent, Modification, Utilisateur
)
import datetime


def prep_db(session, sample_member1, wired_device):
    session.add_all([sample_member1])
    session.commit()

    Utilisateur.find_or_create(session, "BadUser")
    Utilisateur.find_or_create(session, "test")
    Utilisateur.find_or_create(session, "BadUser2")


@pytest.fixture
def api_client(sample_member1, wired_device):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(), sample_member1, wired_device)
        yield c


def test_modification_pass_updated(api_client, sample_member1):
    s = db.get_db().get_session()
    a = Adherent.find(s, sample_member1.login)

    a.start_modif_tracking()
    a.password = "TESTESTEST"
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, a,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        '--- !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n'
        'password:\n'
        '- a\n'
        '- TESTESTEST\n'
    )
    assert m.adherent_id == sample_member1.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2


def test_modification_multiple_changes_updated(api_client, sample_member1):
    s = db.get_db().get_session()
    a = Adherent.find(s, sample_member1.login)

    a.start_modif_tracking()
    a.commentaires = "Hey I am a comment"
    a.nom = "Test"
    a.prenom = "Test"
    a.mail = "ono@no.fr"
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, a,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        '--- !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n'
        'commentaires:\n'
        '- \n'
        '- Hey I am a comment\n'
        'mail:\n'
        '- j.dubois@free.fr\n'
        '- ono@no.fr\n'
        'nom:\n'
        '- Dubois\n'
        '- Test\n'
        'prenom:\n'
        '- Jean-Louis\n'
        '- Test\n'
    )
    assert m.adherent_id == sample_member1.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2


def test_modification_add_new_user(api_client, sample_member2):
    s = db.get_db().get_session()

    a = sample_member2
    s.add(a)
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, a,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        '--- !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n'
        'chambre_id:\n'
        '- \n'
        '- 1\n'
        'commentaires:\n'
        '- \n'
        '- Desauthent pour routeur\n'
        'id:\n'
        '- \n'
        '- 2\n'
        'login:\n'
        '- \n'
        '- reignier\n'
        'mail:\n'
        '- \n'
        '- bgdu78@hotmail.fr\n'
        'mode_association:\n'
        '- \n'
        '- 2011-04-30 17:50:17\n'
        'nom:\n'
        '- \n'
        '- Reignier\n'
        'password:\n'
        '- \n'
        '- a\n'
        'prenom:\n'
        '- \n'
        '- Edouard\n'
    )
    assert m.adherent_id == a.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2


def test_modification_delete_member(api_client, sample_member1):
    s = db.get_db().get_session()
    a = Adherent.find(s, sample_member1.login)

    a.start_modif_tracking()
    s.delete(a)
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, a,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        '--- !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n'
        'chambre_id:\n'
        '- 1\n'
        '- \n'
        'date_de_depart:\n'
        '- 2005-07-14 12:30:00\n'
        '- \n'
        'id:\n'
        '- 1\n'
        '- \n'
        'login:\n'
        '- dubois_j\n'
        '- \n'
        'mail:\n'
        '- j.dubois@free.fr\n'
        '- \n'
        'mode_association:\n'
        '- 2011-04-30 17:50:17\n'
        '- \n'
        'nom:\n'
        '- Dubois\n'
        '- \n'
        'password:\n'
        '- a\n'
        '- \n'
        'prenom:\n'
        '- Jean-Louis\n'
        '- \n'
    )
    assert m.adherent_id == sample_member1.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2


def test_add_device_wired(api_client, wired_device, sample_member1):

    s = db.get_db().get_session()
    s.add(wired_device)
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, wired_device,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        "ordinateur: !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n"
        "adherent_id:\n"
        "- \n"
        "- 1\n"
        "dns:\n"
        "- \n"
        "- bonnet_n4651\n"
        "id:\n"
        "- \n"
        "- 1\n"
        "ip:\n"
        "- \n"
        "- 157.159.42.42\n"
        "ipv6:\n"
        "- \n"
        "- e91f:bd71:56d9:13f3:5499:25b:cc84:f7e4\n"
        "mac:\n"
        "- \n"
        "- 96-24-F6-D0-48-A7\n"
    )
    assert m.adherent_id == sample_member1.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2


def test_add_device_wireless(
                api_client, wireless_device, sample_member1, sample_member2):

    s = db.get_db().get_session()
    s.add(wireless_device)
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, wireless_device,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        "portable: !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n"
        "adherent_id:\n"
        "- \n"
        "- 2\n"
        "id:\n"
        "- \n"
        "- 1\n"
        "mac:\n"
        "- \n"
        "- 80-65-F3-FC-44-A9\n"
    )
    assert m.adherent_id == sample_member2.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2


def test_update_device_wired(api_client, wired_device, sample_member1,
                             sample_member2):

    s = db.get_db().get_session()
    s.add(wired_device)
    s.flush()

    wired_device.start_modif_tracking()
    wired_device.adherent = sample_member2
    wired_device.dns = "hello"
    wired_device.ip = "8.8.8.8"
    wired_device.ipv6 = "fe80::1"
    wired_device.mac = "AB-CD-EF-12-34-56"
    # Build the corresponding modification
    Modification.add_and_commit(s, wired_device,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        "ordinateur: !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n"
        "adherent_id:\n"
        "- 1\n"
        "- 2\n"
        "dns:\n"
        "- bonnet_n4651\n"
        "- hello\n"
        "ip:\n"
        "- 157.159.42.42\n"
        "- 8.8.8.8\n"
        "ipv6:\n"
        "- e91f:bd71:56d9:13f3:5499:25b:cc84:f7e4\n"
        "- fe80::1\n"
        "mac:\n"
        "- 96-24-F6-D0-48-A7\n"
        "- AB-CD-EF-12-34-56\n"
    )
    assert m.adherent_id == sample_member2.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2


def test_update_device_wireless(
                api_client, wireless_device, sample_member1, sample_member2):

    s = db.get_db().get_session()
    s.add(wireless_device)
    s.flush()

    wireless_device.start_modif_tracking()
    wireless_device.adherent = sample_member1
    wireless_device.mac = "12-34-56-78-9A-BD"
    # Build the corresponding modification
    Modification.add_and_commit(s, wireless_device,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        "portable: !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n"
        "adherent_id:\n"
        "- 2\n"
        "- 1\n"
        "mac:\n"
        "- 80-65-F3-FC-44-A9\n"
        "- 12-34-56-78-9A-BD\n"
    )
    assert m.adherent_id == sample_member1.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2


def test_delete_device_wired(api_client, wired_device, sample_member1,
                             sample_member2):

    s = db.get_db().get_session()
    s.add(wired_device)
    s.flush()

    wired_device.start_modif_tracking()
    s.delete(wired_device)
    s.flush()
    # Build the corresponding modification
    Modification.add_and_commit(s, wired_device,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    print(m.action)
    assert m.action == (
        "---\n"
        "ordinateur: Suppression de l'ordinateur 96-24-F6-D0-48-A7\n"
    )
    assert m.adherent_id == sample_member1.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2


def test_delete_device_wireless(
                api_client, wireless_device, sample_member1, sample_member2):

    s = db.get_db().get_session()
    s.add(wireless_device)
    s.flush()

    wireless_device.start_modif_tracking()
    s.delete(wireless_device)
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, wireless_device,
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    print(m.action)
    assert m.action == (
        "---\n"
        "portable: Suppression du portable 80-65-F3-FC-44-A9\n"
    )
    assert m.adherent_id == sample_member2.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 2
