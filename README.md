# Concurseiro AI - Backend (FastAPI) 🧠

Este é o motor de inteligência do **Concurseiro AI**. Construído em Python utilizando FastAPI, atua conectando o usuário final aos LLMs (Large Language Models) do Google Gemini para processar, simplificar e gerar conteúdo educacional de alta qualidade para concursos públicos.

## 🛠️ Tecnologias Utilizadas
- **FastAPI**: API assíncrona, robusta e escalável.
- **SQLAlchemy (Async)**: ORM poderoso preparado para SQLite (desenvolvimento) ou PostgreSQL (produção).
- **Google Generative AI**: SDK do Gemini para a lógica de geração (Questões, Simulados, Planos de Aula).
- **SlowAPI**: Rate Limiting para evitar abusos na camada gratuita de IA.
- **PyMuPDF (fitz)**: Para leitura e extração de texto em uploads de apostilas/PDFs.

## 📦 Como rodar localmente

1. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuração (.env):**
   Crie um arquivo `.env` na raiz do backend baseado no `.env.example`:
   ```env
   GEMINI_API_KEY=sua_chave_aqui
   CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
   # DATABASE_URL=postgresql+asyncpg://user:pass@localhost/concurseiro (Opcional)
   ```

4. **Inicie o servidor local (Uvicorn):**
   ```bash
   uvicorn app.main:app --reload
   ```
   A API estará acessível em `http://localhost:8000` e a documentação interativa (Swagger UI) em `http://localhost:8000/docs`.

## 📁 Estrutura de Pastas
- `app/routers/`: Rotas modulares do sistema (simulados, mentoria, conteúdo).
- `app/services/`: Toda a lógica focada em IA está isolada aqui (`ia_service.py`).
- `app/models.py & crud.py`: Estrutura e manipulação do banco de dados SQLAlchemy.
