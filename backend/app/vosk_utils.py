import os
import wave
import json
import re
import subprocess
from vosk import Model, KaldiRecognizer

# 1️⃣ Chemin vers ton modèle Vosk
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "vosk-model-br-0.8"
)
vosk_model = Model(MODEL_PATH)

def convert_to_wav(input_path: str) -> str:
    """
    Convertit un fichier audio en WAV 16 kHz mono via ffmpeg CLI.
    Retourne le chemin du WAV généré.
    """
    base, _ = os.path.splitext(input_path)
    wav_path = f"{base}_converted.wav"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        wav_path
    ], check=True)
    return wav_path

def transcrire_audio(wav_path: str) -> tuple[str, list]:
    """
    Lit le WAV et collecte le texte brut + liste de mots avec timestamps.
    """
    wf = wave.open(wav_path, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    rec.SetWords(True)

    results = []
    words = []

    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            results.append(result.get("text", ""))
            words.extend(result.get("result", []))

    final = json.loads(rec.FinalResult())
    results.append(final.get("text", ""))
    words.extend(final.get("result", []))

    full_text = " ".join(r for r in results if r)
    return full_text, words


def segmenter_par_pause(words, pause_threshold=0.8):
    """
    Découpe la transcription en phrases selon les pauses détectées dans le flux audio.
    """
    if not words:
        return ""

    phrases = []
    current = [words[0]['word']]
    for i in range(1, len(words)):
        gap = words[i]['start'] - words[i-1]['end']
        if gap > pause_threshold:
            phrases.append(" ".join(current))
            current = []
        current.append(words[i]['word'])

    if current:
        phrases.append(" ".join(current))

    # Mise en forme : majuscule + point final
    formatted = []
    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase:
            continue
        phrase = phrase[0].upper() + phrase[1:]
        if phrase[-1] not in ".!?":
            phrase += "."
        formatted.append(phrase)

    return " ".join(formatted)


# 🔧 Test rapide
if __name__ == "__main__":
    print("== Test de chargement Vosk ==")
    print("MODEL_PATH =", MODEL_PATH)
    try:
        _ = Model(MODEL_PATH)
        print("✔ Modèle chargé avec succès !")
    except Exception as e:
        print("❌ Erreur lors du chargement :", e)
