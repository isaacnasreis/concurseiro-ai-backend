from pydantic import BaseModel, Field
from typing import List

class QuestaoRequest(BaseModel):
    """
    Define a estrutura de dados que esperamos receber do frontend
    para gerar uma questão.
    """
    materia: str = Field(
        ...,
        description="A matéria para a qual a questão deve ser gerada.",
        example="Direito Administrativo"
    )
    topico: str = Field(
        ...,
        description="O tópico específico dentro da matéria.",
        example="Atos Administrativos"
    )
    nivel_dificuldade: str = Field(
        "Médio",
        description="O nível de dificuldade desejado para a questão.",
        example="Fácil"
    )

class QuestaoResponse(BaseModel):
    """
    Define a estrutura de dados que a nossa API irá retornar
    contendo a questão gerada.
    """
    enunciado: str
    alternativas: List[str]
    resposta_correta: str
    comentarios: str = "Nenhum comentário adicional."

    class Config:
        orm_mode = True