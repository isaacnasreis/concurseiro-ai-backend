from fastapi import APIRouter, HTTPException
from ..schemas import MentorRequest, MentorResponse
from ..services.ia_service import gerar_plano_de_aula_ia

router = APIRouter(prefix="/mentor", tags=["Mentor"])

@router.post("/gerar-plano-de-aula", response_model=MentorResponse)
async def gerar_plano_de_aula_endpoint(request: MentorRequest):
    plano_de_aula = await gerar_plano_de_aula_ia(
        materia=request.materia,
        topico=request.topico,
        sub_topico=request.sub_topico
    )

    if not plano_de_aula:
        raise HTTPException(status_code=500, detail="Erro ao gerar o plano de aula com a IA.")
    return plano_de_aula
