# Breizh Translator – Backend 🎙️

Ce dépôt contient le backend FastAPI pour l'application **Klev ha Skriva**, qui transcrit de l’audio breton en texte breton.

---

## 📁 Structure du projet

```
breizh-translator-backend/
├── app/
│ ├── main.py # point d’entrée FastAPI
│ ├── vosk_utils.py # fonctions de transcription & nettoyage
│ ├── models/ # y mettre ton modèle Vosk
│ └── requirements.txt
├── Dockerfile # si tu veux dockeriser
└── README.md
```

---

## 📦 Modèle Vosk – Breton

Le modèle vocal Vosk pour le breton est **trop volumineux (> 100 Mo)** pour être inclus dans le dépôt GitHub.

### 🔽 Installation manuelle

1. Télécharger le modèle ici :  
   https://alphacephei.com/vosk/models  
   Fichier recommandé : `vosk-model-br-0.8.zip`

2. Décompresser et placer le dossier dans :

app/models/vosk-model-br-0.8/


### 🛠️ Installation automatique (optionnelle)

Créer un script `install_models.sh` :

```bash
#!/bin/bash
mkdir -p app/models
cd app/models
wget https://alphacephei.com/vosk/models/vosk-model-br-0.8.zip
unzip vosk-model-br-0.8.zip
rm vosk-model-br-0.8.zip

🚀 Lancer le backend en local

Installer les dépendances Python :
pip install -r app/requirements.txt
Lancer le serveur FastAPI :
uvicorn app.main:app --reload
L'API sera disponible sur : http://localhost:8000

🐳 Docker (optionnel)

Pour builder et exécuter avec Docker :

docker build -t breizh-translator-backend .
docker run -p 8000:8000 breizh-translator-backend
📜 Licence

Projet open-source pour la promotion de la langue bretonne.
Licence : MIT.

🤝 Contributeurs bienvenus !

Des idées, des améliorations, des bugs à corriger ?
Bienvenue dans l’aventure ✊
```