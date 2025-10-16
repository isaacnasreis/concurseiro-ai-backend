from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class Simulado(Base):
    __tablename__ = "simulados"

    id = Column(Integer, primary_key=True, index=True)
    materia = Column(String, index=True)
    topico = Column(String)
    data_realizacao = Column(DateTime, default=datetime.datetime.utcnow)
    
    questoes = relationship("QuestaoRespondida", back_populates="simulado")

class QuestaoRespondida(Base):
    __tablename__ = "questoes_respondidas"

    id = Column(Integer, primary_key=True, index=True)
    enunciado = Column(String)
    resposta_correta = Column(String)
    resposta_usuario = Column(String)
    acertou = Column(String) # "sim" ou "nao"
    simulado_id = Column(Integer, ForeignKey("simulados.id"))

    simulado = relationship("Simulado", back_populates="questoes")