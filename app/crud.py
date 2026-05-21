from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from . import models, schemas

async def salvar_resultado_simulado(db: AsyncSession, resultado: schemas.ResultadoSimuladoRequest):
    db_simulado = models.Simulado(
        materia=resultado.materia,
        topico=resultado.topico,
        session_id=resultado.session_id
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

async def get_estatisticas_por_session(db: AsyncSession, session_id: str):
    stmt_simulados = select(func.count(models.Simulado.id)).where(models.Simulado.session_id == session_id)
    result_simulados = await db.execute(stmt_simulados)
    simulados_count = result_simulados.scalar_one_or_none() or 0

    stmt_questoes = select(
        func.count(models.QuestaoRespondida.id),
        func.sum(case((models.QuestaoRespondida.acertou == 'sim', 1), else_=0))
    ).select_from(models.Simulado).join(models.QuestaoRespondida).where(models.Simulado.session_id == session_id)
    
    result_questoes = await db.execute(stmt_questoes)
    questoes_count, acertos_count = result_questoes.one_or_none() or (0, 0)
    
    if acertos_count is None:
        acertos_count = 0

    taxa_acerto = 0
    if questoes_count > 0:
        taxa_acerto = int((acertos_count / questoes_count) * 100)

    return {
        "simuladosRealizados": simulados_count,
        "questoesRespondidas": questoes_count,
        "taxaAcerto": taxa_acerto
    }