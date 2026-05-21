import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Usa PostgreSQL se definido (ex: postgresql+asyncpg://user:password@host:dbname), senão SQLite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./concurseiroai.db")

# Garante que bancos PostgreSQL fornecidos em formato padrão usem o driver asyncpg
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# O driver asyncpg não reconhece "sslmode=require", ele exige "ssl=require"
if "sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("sslmode=", "ssl=")

engine = create_async_engine(DATABASE_URL, echo=False) # echo=False para produção
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session