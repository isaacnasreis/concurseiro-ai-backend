import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()

try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")
    model = None

def criar_prompt(materia: str, topico: str, nivel: str) -> str:
    """Monta o prompt detalhado para a IA."""
    
    prompt = f"""
    Aja como um especialista em elaboração de questões para concursos públicos no Brasil.
    Seu objetivo é criar uma questão de múltipla escolha (4 alternativas) sobre a matéria '{materia}', 
    focada no tópico específico '{topico}', com um nível de dificuldade '{nivel}'.

    A questão deve seguir estritamente o seguinte formato de saída JSON:
    {{
      "enunciado": "O enunciado completo da questão aqui.",
      "alternativas": [
        "Texto da alternativa A",
        "Texto da alternativa B",
        "Texto da alternativa C",
        "Texto da alternativa D"
      ],
      "resposta_correta": "Texto da alternativa que é a resposta correta.",
      "comentarios": "Um parágrafo explicando o porquê da resposta correta estar certa e, se possível, por que as outras estão erradas."
    }}

    Certifique-se de que o campo "resposta_correta" contenha o texto exato de uma das opções listadas em "alternativas".
    Não adicione nenhuma outra informação ou formatação fora deste objeto JSON.
    """
    return prompt

async def gerar_questao_ia(materia: str, topico: str, nivel: str):
    """
    Chama a API do Gemini para gerar uma questão e garante que a saída seja um JSON válido.
    """
    if not model:
        raise ConnectionError("A configuração da API do Gemini falhou. Verifique a API Key.")

    prompt = criar_prompt(materia, topico, nivel)
    
    try:
        response = model.generate_content(prompt)
        
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        return json.loads(cleaned_response_text)
    except Exception as e:
        print(f"Erro ao gerar ou processar a questão da IA: {e}")
        print(f"Resposta recebida da IA: {response.text if 'response' in locals() else 'Nenhuma resposta recebida'}")
        return None