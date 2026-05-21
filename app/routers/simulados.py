from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import QuestaoRequest, QuestaoResponse, SimuladoRequest, ResultadoSimuladoRequest
from ..services.ia_service import gerar_questao_ia, gerar_simulado_ia
from .. import crud
from ..database import get_db

router = APIRouter(prefix="/simulados", tags=["Simulados"])

@router.post("/gerar-questao", response_model=QuestaoResponse)
async def gerar_questao(request: QuestaoRequest):
    resultado_ia = await gerar_questao_ia(
        materia=request.materia,
        topico=request.topico,
        nivel=request.nivel_dificuldade,
        contexto=request.contexto 
    )

    if not resultado_ia:
        raise HTTPException(status_code=500, detail="Erro ao gerar a questão.")
    return resultado_ia

@router.post("/gerar-simulado", response_model=List[QuestaoResponse])
async def gerar_simulado_endpoint(request: SimuladoRequest):
    questoes = await gerar_simulado_ia(
        materia=request.materia,
        topico=request.topico,
        nivel=request.nivel_dificuldade.value,
        quantidade=request.quantidade_questoes,
        contexto=request.contexto
    )

    if not questoes or len(questoes) < request.quantidade_questoes:
        raise HTTPException(status_code=500, detail="Erro na geração do simulado.")
    return questoes

@router.post("/salvar-simulado/")
async def salvar_simulado(resultado: ResultadoSimuladoRequest, db: AsyncSession = Depends(get_db)):
    await crud.salvar_resultado_simulado(db=db, resultado=resultado)
    return {"status": "Resultados salvos com sucesso!"}
