# app/main.py

import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# from vosk_utils import convert_to_wav, transcrire_audio, nettoyage_simple
from app.vosk_utils import convert_to_wav, transcrire_audio, segmenter_par_pause


# Crée l’application FastAPI
app = FastAPI(
    title="Breizh Translator Backend",
    description="API pour transcrire et nettoyer des fichiers audio bretons via Vosk",
    version="1.0"
)

# Si ton frontend Angular tourne sur un autre port, active le CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Formats audio autorisés
ALLOWED_EXT = {".wav", ".mp3", ".ogg", ".flac", ".m4a", ".mp4"}

@app.post("/upload/", summary="Transcrire et nettoyer un fichier audio")
async def upload_and_transcribe(audio_file: UploadFile = File(...)):
    # 1. Vérifier l'extension
    ext = os.path.splitext(audio_file.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=415, detail=f"Format '{ext}' non supporté")

    # 2. Créer un répertoire temporaire
    tmp_dir = tempfile.mkdtemp()
    try:
        # 3. Sauvegarder le fichier uploadé
        in_path = os.path.join(tmp_dir, audio_file.filename)
        with open(in_path, "wb") as f:
            f.write(await audio_file.read())

        # 4. Convertir en WAV si besoin
        wav_path = in_path if ext == ".wav" else convert_to_wav(in_path)

        # 5. Transcrire le WAV (texte brut)
        raw_text, words = transcrire_audio(wav_path)

        # 6. Nettoyer le texte
        clean_text = segmenter_par_pause(words)

        # 7. Retourner le résultat en JSON
        return JSONResponse({
            "filename": audio_file.filename,
            "raw_text": raw_text,
            "clean_text": clean_text
        })

    finally:
        # 8. Nettoyer les fichiers temporaires
        shutil.rmtree(tmp_dir, ignore_errors=True)
