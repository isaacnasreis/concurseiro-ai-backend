from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio

class NivelDificuldade(str, Enum):
    facil = "Fácil"
    medio = "Médio"
    dificil = "Difícil"

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
    nivel_dificuldade: NivelDificuldade = Field(
        default=NivelDificuldade.medio,
        description="O nível de dificuldade desejado para a questão."
    )
    contexto: Optional[str] = Field(
        default=None, 
        description="Um trecho de texto (material de estudo) para basear a questão."
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

class SimuladoRequest(BaseModel):
    """
    Define os parâmetros para a geração de um simulado completo.
    """
    materia: str = Field(...)
    topico: str = Field(...)
    nivel_dificuldade: NivelDificuldade = Field(...)
    quantidade_questoes: int = Field(
        ..., 
        gt=0, # gt=0 significa "greater than 0" (maior que 0)
        le=10, # le=10 significa "less than or equal to 10" (menor ou igual a 10) - um limite para não sobrecarregar a API
        description="Número de questões para o simulado."
    )
    contexto: Optional[str] = Field(default=None)

class SimplificadorRequest(BaseModel):
    texto_original: str = Field(..., description="O texto a ser processado pela IA.")
    comando: str = Field(
        default="Explique este texto em termos simples para um iniciante em concursos.",
        description="A instrução para a IA sobre como transformar o texto."
    )

class SimplificadorResponse(BaseModel):
    texto_processado: str = Field(..., description="O texto resultante após o processamento da IA.")

class QuestaoResultado(BaseModel):
    enunciado: str
    resposta_correta: str
    resposta_usuario: Optional[str]

class ResultadoSimuladoRequest(BaseModel):
    materia: str
    topico: str
    questoes: List[QuestaoResultado]