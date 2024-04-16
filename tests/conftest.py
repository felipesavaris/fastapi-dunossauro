import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Base, User
from fast_zero.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.Sequence(lambda n: n)
    username = factory.LazyAttribute(lambda obj: f'test{obj.id}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example')


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    # injeta a sessao de testes no depends DB nos endpoints
    with TestClient(app=app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

        app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        # SQLite, usa apenas 1a thread, enquanto o fastapi pode usar várias
        # desativando a linha a seguir, faz com a conexao seja compartilhada com várias threads
        connect_args={'check_same_thread': False},
        # o argumento a seguir faz com que seja possível usar a mesma conexao em todas as solicitaçoes
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    yield Session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = UserFactory(password=get_password_hash('123'))

    session.add(user)
    session.commit()
    session.refresh(user)

    # monkey patching -> add um atributo em tempo de execucao
    user.clean_password = '123'

    return user


@pytest.fixture
def other_user(session):
    user = UserFactory(password=get_password_hash('123'))

    session.add(user)
    session.commit()
    session.refresh(user)

    # monkey patching -> add um atributo em tempo de execucao
    user.clean_password = '123'

    return user
    

@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
