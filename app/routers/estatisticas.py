from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import EstatisticasResponse
from .. import crud
from ..database import get_db

router = APIRouter(prefix="/estatisticas", tags=["Estatisticas"])

@router.get("/{session_id}", response_model=EstatisticasResponse)
async def get_estatisticas(session_id: str, db: AsyncSession = Depends(get_db)):
    """
    Retorna as estatísticas de desempenho para um session_id específico.
    """
    return await crud.get_estatisticas_por_session(db, session_id)
