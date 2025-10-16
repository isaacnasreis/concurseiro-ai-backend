from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def salvar_resultado_simulado(db: AsyncSession, resultado: schemas.ResultadoSimuladoRequest):
    db_simulado = models.Simulado(
        materia=resultado.materia,
        topico=resultado.topico
    )
    db.add(db_simulado)
    await db.commit()
    await db.refresh(db_simulado)

    for questao in resultado.questoes:
        db_questao = models.QuestaoRespondida(
            enunciado=questao.enunciado,
            resposta_correta=questao.resposta_correta,
            resposta_usuario=questao.resposta_usuario,
            acertou="sim" if questao.resposta_usuario == questao.resposta_correta else "nao",
            simulado_id=db_simulado.id
        )
        db.add(db_questao)
    
    await db.commit()
    return db_simulado