import pytest
from adh.model.database import Database as db
from CONFIGURATION import TEST_DATABASE as db_settings
from adh.model.models import (
    Adherent, Chambre, Vlan, Modification, Utilisateur
)
import datetime


@pytest.fixture
def sample_vlan():
    yield Vlan(
        numero=42,
        adresses="192.168.42.1",
        adressesv6="fe80::1",
    )


@pytest.fixture
def sample_room(sample_vlan):
    yield Chambre(
        numero=1234,
        description='chambre 1',
        vlan=sample_vlan,
    )


@pytest.fixture
def sample_member(sample_room):
    yield Adherent(
        nom='Dubois',
        prenom='Jean-Louis',
        mail='j.dubois@free.fr',
        login='dubois_j',
        password='a',
        chambre=sample_room,
    )


@pytest.fixture
def sample_member2(sample_room):
    yield Adherent(
        nom='Reignier',
        prenom='Edouard',
        mail='bgdu78@hotmail.fr',
        login='reignier',
        commentaires='Desauthent pour routeur',
        password='a',
        chambre=sample_room,
    )


def prep_db(session,
            sample_member,
            sample_room, sample_vlan):
    session.add_all([
        sample_room, sample_vlan,
        sample_member])
    session.commit()


@pytest.fixture
def api_client(sample_member, sample_room, sample_vlan):
    from .context import app
    with app.app.test_client() as c:
        db.init_db(db_settings, testing=True)
        prep_db(db.get_db().get_session(),
                sample_member,
                sample_room,
                sample_vlan)
        yield c


def test_modification_pass_updated(api_client, sample_member):
    s = db.get_db().get_session()
    a = Adherent.find(s, sample_member.login)

    a.start_modif_tracking()
    a.password = "TESTESTEST"
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, a, a.get_ruby_modif(),
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        '--- !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n'
        'password:\n'
        '- a\n'
        '- TESTESTEST\n'
    )
    assert m.adherent_id == sample_member.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 1


def test_modification_multiple_changes_updated(api_client, sample_member):
    s = db.get_db().get_session()
    a = Adherent.find(s, sample_member.login)

    a.start_modif_tracking()
    a.commentaires = "Hey I am a comment"
    a.nom = "Test"
    a.prenom = "Test"
    a.mail = "ono@no.fr"
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, a, a.get_ruby_modif(),
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
    assert m.adherent_id == sample_member.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 1


def test_modification_add_new_user(api_client, sample_member2):
    s = db.get_db().get_session()

    a = sample_member2
    s.add(a)
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, a, a.get_ruby_modif(),
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
    assert m.utilisateur_id == 1


def test_modification_delete_member(api_client, sample_member):
    s = db.get_db().get_session()
    a = Adherent.find(s, sample_member.login)

    a.start_modif_tracking()
    s.delete(a)
    s.flush()

    # Build the corresponding modification
    Modification.add_and_commit(s, a, a.get_ruby_modif(),
                                Utilisateur.find_or_create(s, "test"))
    q = s.query(Modification)
    m = q.first()
    assert m.action == (
        '--- !ruby/hash:ActiveSupport::HashWithIndifferentAccess\n'
        'chambre_id:\n'
        '- 1\n'
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
    assert m.adherent_id == sample_member.id
    now = datetime.datetime.now()
    one_sec = datetime.timedelta(seconds=1)
    assert now - m.created_at < one_sec
    assert now - m.updated_at < one_sec
    assert m.utilisateur_id == 1
