from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz
from .schemas import (
    QuestaoRequest, QuestaoResponse, SimuladoRequest, 
    SimplificadorRequest, SimplificadorResponse, ResultadoSimuladoRequest
)
from .services.ia_service import (
    gerar_questao_ia, gerar_simulado_ia, simplificar_texto_ia
)
from typing import List
from . import models, crud
from .database import engine, SessionLocal
import asyncio
from contextlib import asynccontextmanager

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código a ser executado na inicialização
    await create_db_and_tables()
    yield
    # Código a ser executado na finalização (se necessário)

app = FastAPI(
    title="ConcurseiroAI API",
    description="API para gerar questões de concursos públicos utilizando IA.",
    version="0.1.0",
    lifespan=lifespan
)

# --- CONFIGURAÇÃO DO CORS ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],    # Permite todos os cabeçalhos
)
# --- FIM DA CONFIGURAÇÃO DO CORS ---

async def get_db():
    async with SessionLocal() as session:
        yield session

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

@app.get("/")
async def read_root():
    """
    Endpoint raiz da aplicação. Retorna uma mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo à API do ConcurseiroAI!"}

@app.get("/status")
async def get_status():
    """
    Endpoint para verificar o status da API.
    """
    return {"status": "ok", "message": "API está funcionando corretamente."}

@app.post("/extrair-contexto-arquivo/")
async def extrair_contexto_arquivo(arquivo: UploadFile = File(...)):
    """
    Recebe um arquivo (.txt ou .pdf), lê seu conteúdo e o retorna como uma string.
    """
    filename = arquivo.filename
    conteudo_texto = ""

    conteudo_bytes = await arquivo.read()

    try:
        if filename.endswith(".txt"):
            conteudo_texto = conteudo_bytes.decode("utf-8")
        
        elif filename.endswith(".pdf"):
            with fitz.open(stream=conteudo_bytes, filetype="pdf") as doc:
                for page in doc:
                    conteudo_texto += page.get_text()
        
        else:
            raise HTTPException(
                status_code=400, 
                detail="Formato de arquivo inválido. Por favor, envie um .txt ou .pdf"
            )
            
        return {"contexto": conteudo_texto, "nome_arquivo": filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Não foi possível processar o arquivo: {e}")

@app.post("/gerar-questao", response_model=QuestaoResponse)
async def gerar_questao(request: QuestaoRequest):
    """
    Recebe os detalhes da questão e retorna uma questão gerada (mockada).
    """
    print(f"Recebido pedido para gerar questão de {request.materia} sobre {request.topico}.")

    resultado_ia = await gerar_questao_ia(
        materia=request.materia,
        topico=request.topico,
        nivel=request.nivel_dificuldade,
        contexto=request.contexto 
    )

    if not resultado_ia:
        raise HTTPException(
            status_code=500, 
            detail="Ocorreu um erro ao gerar a questão com a IA. Tente novamente."
        )

    return resultado_ia

@app.post("/gerar-simulado", response_model=List[QuestaoResponse])
async def gerar_simulado_endpoint(request: SimuladoRequest):
    """
    Recebe os parâmetros e gera um simulado completo com várias questões.
    """
    print(f"Iniciando geração de simulado com {request.quantidade_questoes} questões.")

    questoes = await gerar_simulado_ia(
        materia=request.materia,
        topico=request.topico,
        nivel=request.nivel_dificuldade.value,
        quantidade=request.quantidade_questoes,
        contexto=request.contexto
    )

    if not questoes or len(questoes) < request.quantidade_questoes:
        raise HTTPException(
            status_code=500,
            detail=f"A IA conseguiu gerar apenas {len(questoes)} de {request.quantidade_questoes} questões. Tente novamente."
        )

    return questoes

@app.post("/simplificar-texto", response_model=SimplificadorResponse)
async def simplificar_texto_endpoint(request: SimplificadorRequest):
    """
    Recebe um texto e um comando, e retorna o texto processado pela IA.
    """
    resultado = await simplificar_texto_ia(
        texto=request.texto_original, 
        comando=request.comando
    )

    if not resultado:
        raise HTTPException(
            status_code=500,
            detail="Ocorreu um erro ao processar o texto com a IA."
        )
    
    return resultado

@app.post("/salvar-simulado/")
async def salvar_simulado(
    resultado: ResultadoSimuladoRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Recebe os resultados de um simulado concluído e salva no banco de dados.
    """
    await crud.salvar_resultado_simulado(db=db, resultado=resultado)
    return {"status": "Resultados salvos com sucesso!"}