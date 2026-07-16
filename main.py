import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ---------- 1. Initialisation de FastAPI ----------
app = FastAPI(title="ISI Chatbot API", description="RAG sur les documents de l'ISI")

# CORS pour permettre les appels depuis un frontend (optionnel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 2. Connexion à la base et chargement du modèle ----------
# Connexion PostgreSQL
conn = psycopg2.connect(os.getenv("DATABASE_URL"))

# Chargement du modèle d'embeddings (il reste en mémoire pour être rapide)
print("🔄 Chargement du modèle SentenceTransformer...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Modèle d'embeddings prêt.")

# ---------- 3. Initialisation du client GroqCloud ----------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- 4. Modèle de données pour la requête ----------
class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3  # Nombre de passages à récupérer

# ---------- 5. Endpoint principal ----------
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        # Étape A : Générer l'embedding de la question
        question_embedding = embedding_model.encode(request.question).tolist()

        # Étape B : Recherche vectorielle dans PostgreSQL
        cur = conn.cursor()
        cur.execute("""
            SELECT content, embedding <=> %s::vector AS distance
            FROM documents
            ORDER BY distance
            LIMIT %s;
        """, (question_embedding, request.top_k))
        
        results = cur.fetchall()
        cur.close()

        if not results:
            return {"answer": "Je n'ai trouvé aucun passage pertinent dans les documents pour répondre à cette question."}

        # Étape C : Construction du contexte
        context = "\n\n---\n\n".join([row[0] for row in results])
        
        # Étape D : Appel à GroqCloud (LLM)
        system_prompt = (
            "Tu es un assistant virtuel de l'Institut Supérieur d'Informatique (ISI). "
            "Réponds à la question de l'utilisateur en utilisant UNIQUEMENT le contexte fourni ci-dessous. "
            "Si la réponse ne se trouve pas dans le contexte, dis clairement que tu ne sais pas, sans inventer d'informations.\n\n"
            "### CONTEXTE :\n" + context
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.question}
            ],
            model="llama-3.1-8b-instant", # Excellent rapport qualité/vitesse sur Groq
            temperature=0.3,
            max_tokens=500,
        )

        answer = chat_completion.choices[0].message.content

        # (Optionnel) Renvoyer aussi les sources pour le debug
        return {
            "answer": answer,
            "sources": [{"content": row[0][:200] + "...", "distance": row[1]} for row in results]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------- 6. Endpoint de santé ----------
@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "Le chatbot ISI est opérationnel !"}