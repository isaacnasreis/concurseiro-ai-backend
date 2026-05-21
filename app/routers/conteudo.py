from fastapi import APIRouter, HTTPException, UploadFile, File
import fitz
from ..schemas import SimplificadorRequest, SimplificadorResponse
from ..services.ia_service import simplificar_texto_ia

router = APIRouter(prefix="/conteudo", tags=["Conteudo"])

@router.post("/extrair-contexto-arquivo/")
async def extrair_contexto_arquivo(arquivo: UploadFile = File(...)):
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
            raise HTTPException(status_code=400, detail="Formato de arquivo inválido.")
            
        return {"contexto": conteudo_texto, "nome_arquivo": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o arquivo: {e}")

@router.post("/simplificar-texto", response_model=SimplificadorResponse)
async def simplificar_texto_endpoint(request: SimplificadorRequest):
    resultado = await simplificar_texto_ia(
        texto=request.texto_original, 
        comando=request.comando
    )

    if not resultado:
        raise HTTPException(status_code=500, detail="Erro ao processar texto.")
    return resultado
