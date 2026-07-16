# Chatbot ISI - Assistant Virtuel de l'Institut Supérieur d'Informatique

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://postgresql.org)
[![GroqCloud](https://img.shields.io/badge/GroqCloud-LLM-orange.svg)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Présentation

**Chatbot ISI** est un assistant conversationnel intelligent basé sur la technologie RAG (Retrieval-Augmented Generation). Il permet de poser des questions sur l'Institut Supérieur d'Informatique (ISI) et d'obtenir des réponses précises et contextualisées à partir des documents officiels de l'établissement.

### Objectif du Projet
- Fournir un accès rapide et fiable aux informations sur l'ISI
- Réduire le temps de recherche d'information pour les étudiants et collaborateurs
- Démontrer l'application des technologies d'IA et de recherche vectorielle

---

## Fonctionnalités

### Backend
-  **Ingestion de documents PDF** : Extraction, découpage et indexation sémantique
-  **Recherche vectorielle** : Utilisation de PostgreSQL + pgVector
-  **Génération d'embeddings** : Modèle SentenceTransformers (`all-MiniLM-L6-v2`)
-  **LLM intégré** : Appel à GroqCloud (modèle `llama-3.1-8b-instant`)
-  **API REST** : Endpoint `/ask` pour interroger le chatbot
-  **Documentation Swagger** : Interface interactive `/docs`

### Frontend
-  **Interface type ChatGPT** : Design moderne et épuré
-  **Conversation fluide** : Messages alternés utilisateur/bot
-  **Indicateur de saisie** : Feedback visuel pendant la génération
-  **Sources affichées** : Transparence sur les passages utilisés
-  **Historique des conversations** : Sauvegarde en mémoire locale
-  **Responsive** : Adapté aux mobiles, tablettes et desktop
-  **Sidebar latérale** : Navigation et nouvelle conversation

---

## Architecture Technique

 Frontend (HTML/CSS/JS)                                      
 Interface type ChatGPT  
         |
        HTTP
 Backend (FastAPI)                                           
 Endpoints : /ask, /health, /static                  
 

  - PostgreSQL + pgVector     - GroqCloud (LLM)          
  - Stockage des vecteurs     - Génération réponse     
  - Recherche sémantique      - Modèle LLM             
            

 - SentenceTransformers     
 - Embeddings local       
 - Modèle all-MiniLM      


### Stack Technique
| Composant | Technologie | Version |
|-----------|-------------|---------|
| **Backend** | FastAPI   | 0.115+  |
| **Base de données** | PostgreSQL + pgVector | 16+ |
| **Embeddings** | SentenceTransformers | 2.2+      |
| **LLM** | GroqCloud (llama-3.1-8b-instant) | API v1 |
| **Frontend** | HTML5 + CSS3 + Vanilla JS | - |
| **Containerisation** | Docker / Docker Compose | - |
| **Langage** | Python | 3.10+ |

---

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Docker** et **Docker Compose** (pour la base de données)
- **Python 3.10 ou supérieur**
- **pip** (gestionnaire de paquets Python)
- **Git** (pour cloner le projet)
- **Compte GroqCloud** : [https://console.groq.com](https://console.groq.com) (gratuit)

---

## 🚀 Installation

### 1. Cloner le dépôt
git clone <url-de-votre-depot>
cd chatbot-isi

## Créer et activer l'environnement virtuel

python3 -m venv venv
source venv/bin/activate  # Sur Linux/Mac
## ou
venv\Scripts\activate     # Sur Windows

## Installer les dépendances
pip install -r requirements.txt

## Lancer la base de données avec Docker
docker compose up -d

## Vérification :La base tourne sur localhost:5433
docker ps

## Configurer les variables d'environnement
### Créez un fichier .env à la racine :
DATABASE_URL=postgresql://admin:admin123@localhost:5433/isi_knowledge
GROQ_API_KEY=votre_clé_api_groq

## Générer le document PDF de connaissances
Créer un document nommée : "document.pdf" et ajouter cela dans la racine du projet pour constituer la mémoire du projet

## Ingérer le PDF dans la base de données
python ingest.py

Cette opération :
 - Extrait le texte du PDF
 - Découpe en segments cohérents
 - Génère des embeddings vectoriels
 - Stocke le tout dans PostgreSQL

## Utilisation

### Démarrer le serveur API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Le serveur est accessible à : http://localhost:8000

### Accéder au Frontend
Le frontend est accessible à : http://localhost:8000/static/index.html

## Structure du projet
chatbot-isi/
├── static/                     # Frontend

│   └── index.html                 # Interface

│
├── venv/                       # Environnement virtuel (ignoré)

│
├── main.py                     # API FastAPI (backend)

├── ingest.py                   # Script d'ingestion PDF

├── document.pdf                # Données ISI (généré)

├── docker-compose.yml          # Configuration Docker

├── requirements.txt            # Dépendances Python

├── .env                        # Variables d'environnement (ignoré)

├── .gitignore                  # Fichiers ignorés par Git
└── README.md                   # Ce fichier

## Contact

**Auteur** : Jean-Leon KABOBI

**Email** : kabobi.jeanleon.dev@gmail.com

**Projet** : Chatbot ISI - Projet M1 GL
