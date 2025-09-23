from fastapi import FastAPI
from .schemas import QuestaoRequest, QuestaoResponse

app = FastAPI(
    title="ConcurseiroAI API",
    description="API para gerar questões de concursos públicos utilizando IA.",
    version="0.1.0"
)

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

    return QuestaoResponse(
        enunciado=f"Qual é a principal característica dos Atos Administrativos no tópico de {request.topico}?",
        alternativas=[
            "Alternativa A",
            "Alternativa B",
            "Alternativa C",
            "Alternativa D"
        ],
        resposta_correta="Alternativa A",
        comentarios="Este é um comentário explicando a resposta correta."
    )