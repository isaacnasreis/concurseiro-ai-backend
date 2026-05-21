import os
from google import genai
import json
from dotenv import load_dotenv
from typing import Optional, List, Dict
import asyncio

load_dotenv()

try:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    # O modelo gemini-3.5-flash é a versão mais avançada do flash e possui 
    # cota generosa no plano gratuito, diferente dos 2.5 que estão limitados.
    MODEL_ID = 'gemini-3.5-flash'
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")
    client = None

def criar_prompt(materia: str, topico: str, nivel: str, contexto: Optional[str] = None) -> str:
    """Monta o prompt detalhado para a IA, adaptando-o se um contexto for fornecido."""

    prompt_base = f"""
    Aja como um especialista em elaboração de questões para concursos públicos no Brasil.
    Seu objetivo é criar uma questão de múltipla escolha (4 alternativas) sobre a matéria '{materia}', 
    focada no tópico específico '{topico}', com um nível de dificuldade '{nivel}'.
    """
    
    if contexto:
        prompt_contexto = f"""

    A questão DEVE ser elaborada utilizando EXCLUSIVAMENTE o seguinte texto de contexto fornecido. Não utilize nenhum conhecimento externo a este texto.

    --- TEXTO DE CONTEXTO ---
    {contexto}
    --- FIM DO TEXTO DE CONTEXTO ---
    """
        prompt_final = prompt_base + prompt_contexto
    else:
        prompt_final = prompt_base

    # A especificação do formato de saída vem no final
    prompt_formato_saida = """

    A questão deve seguir estritamente o seguinte formato de saída JSON:
    {
      "enunciado": "O enunciado completo da questão aqui.",
      "alternativas": [
        "Texto da alternativa A",
        "Texto da alternativa B",
        "Texto da alternativa C",
        "Texto da alternativa D"
      ],
      "resposta_correta": "Texto da alternativa que é a resposta correta.",
      "comentarios": "Um parágrafo explicando o porquê da resposta correta estar certa, baseado no contexto se fornecido."
    }

    Certifique-se de que o campo "resposta_correta" contenha o texto exato de uma das opções listadas em "alternativas".
    Não adicione nenhuma outra informação ou formatação fora deste objeto JSON.
    """

    return prompt_final + prompt_formato_saida

async def gerar_questao_ia(materia: str, topico: str, nivel: str, contexto: Optional[str] = None) -> Optional[Dict]:
    """
    Chama a API do Gemini para gerar uma questão e garante que a saída seja um JSON válido.
    """
    if not client:
        raise ConnectionError("A configuração da API do Gemini falhou. Verifique a API Key.")

    prompt = criar_prompt(materia, topico, nivel, contexto)
    
    try:
        response = await asyncio.to_thread(client.models.generate_content, model=MODEL_ID, contents=prompt)
        
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        return json.loads(cleaned_response_text)
    except Exception as e:
        print(f"Erro ao gerar ou processar a questão da IA: {e}")
        print(f"Resposta recebida da IA: {response.text if 'response' in locals() else 'Nenhuma resposta recebida'}")
        return None

def criar_prompt_simulado(materia: str, topico: str, nivel: str, quantidade: int, contexto: Optional[str] = None) -> str:
    prompt_base = f"""
    Aja como um especialista em elaboração de questões para concursos públicos no Brasil.
    Seu objetivo é criar {quantidade} questões inéditas de múltipla escolha (4 alternativas cada) sobre a matéria '{materia}', 
    focadas no tópico específico '{topico}', com um nível de dificuldade '{nivel}'.
    """
    
    if contexto:
        prompt_contexto = f"""

    As questões DEVEM ser elaboradas utilizando EXCLUSIVAMENTE o seguinte texto de contexto fornecido. Não utilize nenhum conhecimento externo a este texto.

    --- TEXTO DE CONTEXTO ---
    {contexto}
    --- FIM DO TEXTO DE CONTEXTO ---
    """
        prompt_final = prompt_base + prompt_contexto
    else:
        prompt_final = prompt_base

    prompt_formato_saida = """

    Você DEVE retornar a resposta ESTRITAMENTE como um ARRAY JSON contendo os objetos das questões.
    Exemplo do formato de saída:
    [
      {
        "enunciado": "O enunciado da questão 1 aqui.",
        "alternativas": ["A1", "A2", "A3", "A4"],
        "resposta_correta": "A1",
        "comentarios": "Por que a A1 está correta."
      },
      {
        "enunciado": "O enunciado da questão 2 aqui.",
        "alternativas": ["B1", "B2", "B3", "B4"],
        "resposta_correta": "B2",
        "comentarios": "Por que a B2 está correta."
      }
    ]

    Certifique-se de que o campo "resposta_correta" contenha o texto exato de uma das opções listadas em "alternativas".
    Retorne APENAS o array JSON válido, sem NENHUM texto antes ou depois, e sem marcações markdown como ```json.
    """

    return prompt_final + prompt_formato_saida

async def gerar_simulado_ia(materia: str, topico: str, nivel: str, quantidade: int, contexto: Optional[str] = None) -> List[Dict]:
    """
    Gera uma lista de questões em uma única chamada de API (otimizado e livre de rate limit).
    """
    if not client:
        raise ConnectionError("A configuração da API do Gemini falhou.")

    prompt = criar_prompt_simulado(materia, topico, nivel, quantidade, contexto)
    
    try:
        response = await asyncio.to_thread(client.models.generate_content, model=MODEL_ID, contents=prompt)
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        questoes = json.loads(cleaned_response_text)
        
        if isinstance(questoes, list):
            return questoes
        else:
            print("Erro: A IA não retornou uma lista.")
            return []
    except Exception as e:
        print(f"Erro ao gerar o simulado com a IA: {e}")
        print(f"Resposta recebida da IA: {response.text if 'response' in locals() else 'Nenhuma resposta recebida'}")
        return []

async def simplificar_texto_ia(texto: str, comando: str) -> Optional[Dict]:
    """
    Usa a IA para processar um texto com base em um comando específico.
    """
    if not client:
        raise ConnectionError("A configuração da API do Gemini falhou.")

    prompt = f"""
    Aja como um tutor especialista em concursos públicos com excelente didática.
    Sua tarefa é reprocessar o texto fornecido abaixo de acordo com o comando do usuário.
    Seja claro, objetivo e use uma linguagem acessível.

    --- COMANDO DO USUÁRIO ---
    {comando}

    --- TEXTO ORIGINAL ---
    {texto}

    --- RESULTADO ---
    """
    
    try:
        response = await asyncio.to_thread(client.models.generate_content, model=MODEL_ID, contents=prompt)
        return {"texto_processado": response.text}
    except Exception as e:
        print(f"Erro ao processar texto com a IA: {e}")
        return None
    
async def gerar_plano_de_aula_ia(materia: str, topico: str, sub_topico: Optional[str] = None) -> Optional[Dict]:
    """
    Gera um plano de aula estruturado sobre um tópico específico.
    """
    if not client:
        raise ConnectionError("A configuração da API do Gemini falhou.")

    topico_completo = f"{topico}: {sub_topico}" if sub_topico else topico

    prompt = f"""
    Aja como um mentor experiente para concursos públicos, especialista na matéria de '{materia}'.
    Sua tarefa é criar um mini plano de aula sobre o tópico específico: '{topico_completo}'.
    O público-alvo é um estudante para o cargo de Analista de Sistemas da Prefeitura de Contagem-MG.
    Seja didático, direto ao ponto e focado no que realmente importa para a prova.

    Retorne sua resposta ESTRITAMENTE no seguinte formato JSON, sem nenhum texto ou formatação adicional:
    {{
      "explicacao_simples": "Uma explicação clara e concisa do conceito, como se estivesse explicando para um colega.",
      "pontos_chave": [
        "Um ponto crucial ou palavra-chave para memorizar.",
        "Outro ponto importante que costuma ser pegadinha.",
        "Um terceiro ponto essencial."
      ],
      "como_cai_em_prova": "Descreva como este tópico é tipicamente cobrado em provas de concurso para a área de TI, mencionando o estilo de bancas como FGV, Cesgranrio, etc.",
      "questao_exemplo": {{
        "enunciado": "Crie aqui um enunciado de uma questão de múltipla escolha (4 alternativas) sobre o tópico.",
        "alternativas": [
          "Texto da alternativa A.",
          "Texto da alternativa B.",
          "Texto da alternativa C.",
          "Texto da alternativa D."
        ],
        "resposta_correta": "O texto exato de uma das alternativas acima.",
        "comentarios": "Um breve comentário explicando por que a resposta está correta."
      }}
    }}
    """

    try:
        response = await asyncio.to_thread(client.models.generate_content, model=MODEL_ID, contents=prompt)
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response_text)
    except Exception as e:
        print(f"Erro ao gerar plano de aula: {e}\nResposta recebida: {response.text if 'response' in locals() else 'N/A'}")
        return None