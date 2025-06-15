# Breizh Translator – Backend 🎙️

Ce dépôt contient le backend FastAPI pour l'application **Klev ha Skriva**, qui transcrit de l’audio breton en texte breton.

---

## 📁 Structure du projet

```
breizh-translator-backend/
├── app/
│   ├── main.py           # Point d’entrée FastAPI
│   ├── vosk_utils.py     # Fonctions de transcription & nettoyage
│   ├── models/           # Y mettre ton modèle Vosk
│   └── requirements.txt
├── Dockerfile            # Si tu veux dockeriser
└── README.md
```

---

## 📦 Modèle Vosk – Breton

Le modèle vocal Vosk pour le breton est **trop volumineux (> 100 Mo)** pour être inclus dans ce dépôt GitHub.

### 🔽 Installation manuelle

1. Télécharger le modèle depuis :  
   👉 https://alphacephei.com/vosk/models  
   👉 Modèle recommandé : `vosk-model-br-0.8.zip`

2. Décompresser l’archive et placer le dossier ici :  
   `app/models/vosk-model-br-0.8/`

### 🛠️ Installation automatique (optionnelle)

Créer un script `install_models.sh` :

```bash
#!/bin/bash
mkdir -p app/models
cd app/models
wget https://alphacephei.com/vosk/models/vosk-model-br-0.8.zip
unzip vosk-model-br-0.8.zip
rm vosk-model-br-0.8.zip
```

Rends-le exécutable avec :
```bash
chmod +x install_models.sh
```

Puis lance-le :
```bash
./install_models.sh
```

---

## 🚀 Lancer le backend en local

### 1. Installer les dépendances Python

```bash
pip install -r app/requirements.txt
```

### 2. Lancer le serveur FastAPI

```bash
uvicorn app.main:app --reload
```

L'API sera disponible sur :  
👉 `http://localhost:8000`

---

## 🐳 Docker (optionnel)

### Builder et lancer l’image :

```bash
docker build -t breizh-translator-backend .
docker run -p 8000:8000 breizh-translator-backend
```

---

## 📜 Licence

Projet open-source pour la promotion de la langue bretonne.  
Licence : **MIT**

---

## 🤝 Contributeurs bienvenus !

Des idées 💡 ?  
Des améliorations 🔧 ?  
Des bugs 🐛 ?  
Bienvenue dans l’aventure ✊
