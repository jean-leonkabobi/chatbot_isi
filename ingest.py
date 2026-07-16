import os
import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import re
from dotenv import load_dotenv

load_dotenv()

# 1. Connexion à PostgreSQL
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# 2. Création de la table avec pgvector (si elle n'existe pas)
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(384)  -- 384 dimensions pour all-MiniLM-L6-v2
    );
""")
conn.commit()

# 3. Chargement du modèle d'embeddings (il va télécharger ~90 Mo une seule fois)
print("🔄 Chargement du modèle d'embeddings (all-MiniLM-L6-v2)...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Modèle chargé !")

# 4. Fonction pour découper le texte en chunks cohérents
def chunk_text(text, chunk_size=500, overlap=50):
    # Nettoie les retours à la ligne et espaces
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# 5. Lecture du PDF (mettez votre PDF dans le même dossier, nommé "document.pdf")
pdf_path = "document.pdf"  # <--- CHANGEZ LE NOM SI BESOIN
if not os.path.exists(pdf_path):
    print(f"❌ Erreur : Le fichier {pdf_path} n'existe pas. Placez un PDF dans le dossier.")
    exit()

print(f"📄 Lecture du PDF : {pdf_path}")
reader = PdfReader(pdf_path)
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() or ""

print(f"📝 Texte extrait : {len(full_text)} caractères.")

# 6. Découpage en chunks
chunks = chunk_text(full_text)
print(f"✂️  Découpage en {len(chunks)} segments.")

# 7. Génération des embeddings et insertion en BATCH (optimisé)
print("🧠 Génération des embeddings (cela peut prendre 1-2 minutes)...")
embeddings = model.encode(chunks, convert_to_numpy=True)

# Préparation des données pour l'insertion en masse
data_to_insert = [(chunk, emb.tolist()) for chunk, emb in zip(chunks, embeddings)]

print("💾 Insertion dans PostgreSQL (pgVector)...")
execute_values(
    cur,
    "INSERT INTO documents (content, embedding) VALUES %s",
    data_to_insert,
    template="(%s, %s::vector)"
)
conn.commit()

print(f"✅ Succès ! {len(chunks)} segments indexés dans la base.")
cur.close()
conn.close()