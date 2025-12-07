from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import  AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///./users.db"

engine = create_async_engine(
    DATABASE_URL, echo=False, future=True, connect_args={"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

