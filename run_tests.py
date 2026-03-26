import os
import csv
import subprocess

from scoring import similarity_percent, label_score, normalize_text

# Lee lista desde txt si existe; si no, usa la lista por defecto
def cargar_lista_pruebas(txt_path="lista_pruebas.txt"):
    if os.path.exists(txt_path):
        palabras = []
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                palabras.append(line)
        return palabras
    return [
        "peyu","kayo","paku","tena","boti","gapi","aku","peta","kato","mipa",
        "patu","tupa","napo","kanu","tapi","tuko","pata","katu","tiko"
    ]

WORDS = cargar_lista_pruebas()

AUDIO_DIR = "audio"
OUT_DIR = "resultados"
OUT_CSV = os.path.join(OUT_DIR, "resultados_pruebas.csv")

os.makedirs(OUT_DIR, exist_ok=True)

with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "archivo",
        "objetivo_esperado",
        "salida_asr",
        "similitud_percent",
        "evaluacion",
        "comentario"
    ])

    for w in WORDS:
        wav = os.path.join(AUDIO_DIR, f"{w}.wav")
        if not os.path.exists(wav):
            writer.writerow([f"{w}.wav", w, "", 0.0, "NO", "Archivo no encontrado"])
            continue

        result = subprocess.run(
            ["python", "asr_es.py", wav],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        out = (result.stdout or "").strip().splitlines()
        transcription = ""
        for line in out[::-1]:
            if line.strip():
                transcription = line.strip()
                break

        # limpieza si viene con prefijo
        if transcription.lower().startswith("transcripción:"):
            transcription = transcription.split(":", 1)[1].strip()

        # scoring (normalizando)
        score = similarity_percent(w, transcription)
        eval_ = label_score(score, ok=90.0, partial=70.0)

        comentario = ""
        if normalize_text(w) != normalize_text(transcription):
            comentario = "Diferencia entre esperado y detectado (normalizado)."

        writer.writerow([f"{w}.wav", w, transcription, score, eval_, comentario])

print(f"Listo. Resultados guardados en: {OUT_CSV}")