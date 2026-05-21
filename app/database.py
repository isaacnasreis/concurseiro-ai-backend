import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Usa PostgreSQL se definido (ex: postgresql+asyncpg://user:password@host:dbname), senão SQLite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./concurseiroai.db")

engine = create_async_engine(DATABASE_URL, echo=False) # echo=False para produção
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()