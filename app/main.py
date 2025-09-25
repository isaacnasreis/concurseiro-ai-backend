from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import QuestaoRequest, QuestaoResponse
from .services.ia_service import gerar_questao_ia

app = FastAPI(
    title="ConcurseiroAI API",
    description="API para gerar questões de concursos públicos utilizando IA.",
    version="0.1.0"
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