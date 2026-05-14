import pytest
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from agent_scaffold.infra.db.repository import SQLAlchemyRepository
from agent_scaffold.infra.db.session import Base, get_session, close_db


class _TestBase(DeclarativeBase):
    pass


class UserModel(_TestBase):
    __tablename__ = "test_users"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    created_at = Column(String(30), nullable=True)
    updated_at = Column(String(30), nullable=True)


@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(_TestBase.metadata.create_all)

    factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_and_get(db_session: AsyncSession) -> None:
    repo = SQLAlchemyRepository(UserModel, db_session)
    user = UserModel(id="1", name="alice", email="alice@example.com")
    created = await repo.create(user)
    assert created.id == "1"
    assert created.name == "alice"

    fetched = await repo.get("1")
    assert fetched is not None
    assert fetched.name == "alice"
    assert fetched.email == "alice@example.com"


@pytest.mark.asyncio
async def test_get_multi(db_session: AsyncSession) -> None:
    repo = SQLAlchemyRepository(UserModel, db_session)
    for i in range(5):
        await repo.create(UserModel(id=str(i), name=f"user{i}", email=f"user{i}@example.com"))

    users = await repo.get_multi(limit=3)
    assert len(users) == 3

    users = await repo.get_multi(offset=3, limit=10)
    assert len(users) == 2


@pytest.mark.asyncio
async def test_update(db_session: AsyncSession) -> None:
    repo = SQLAlchemyRepository(UserModel, db_session)
    user = await repo.create(UserModel(id="1", name="bob", email="bob@example.com"))

    updated = await repo.update("1", UserModel(id="1", name="bobby", email="bob@example.com"))
    assert updated is not None
    assert updated.name == "bobby"


@pytest.mark.asyncio
async def test_delete(db_session: AsyncSession) -> None:
    repo = SQLAlchemyRepository(UserModel, db_session)
    await repo.create(UserModel(id="1", name="charlie", email="c@example.com"))
    assert await repo.count() == 1

    result = await repo.delete("1")
    assert result is True
    assert await repo.count() == 0


@pytest.mark.asyncio
async def test_delete_nonexistent(db_session: AsyncSession) -> None:
    repo = SQLAlchemyRepository(UserModel, db_session)
    result = await repo.delete("nonexistent-id")
    assert result is False


@pytest.mark.asyncio
async def test_count(db_session: AsyncSession) -> None:
    repo = SQLAlchemyRepository(UserModel, db_session)
    assert await repo.count() == 0
    await repo.create(UserModel(id="1", name="a", email="a@example.com"))
    await repo.create(UserModel(id="2", name="b", email="b@example.com"))
    assert await repo.count() == 2


@pytest.mark.asyncio
async def test_update_nonexistent(db_session: AsyncSession) -> None:
    repo = SQLAlchemyRepository(UserModel, db_session)
    result = await repo.update("nonexistent-id", UserModel(id="x", name="x", email="x@example.com"))
    assert result is None
