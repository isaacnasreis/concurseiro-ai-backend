from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, SessionLocal
import asyncio
from contextlib import asynccontextmanager
import os
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .routers import simulados, conteudo, mentor, estatisticas

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando a API do ConcurseiroAI...")
    await create_db_and_tables()
    yield
    logger.info("Finalizando a API...")

app = FastAPI(
    title="ConcurseiroAI API",
    description="API para gerar questões de concursos públicos utilizando IA.",
    version="0.1.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulados.router)
app.include_router(conteudo.router)
app.include_router(mentor.router)
app.include_router(estatisticas.router)

@app.get("/")
@limiter.limit("10/minute")
async def read_root(request: Request):
    return {"message": "Bem-vindo à API do ConcurseiroAI!"}

@app.get("/status")
async def get_status():
    return {"status": "ok", "message": "API está funcionando corretamente."}