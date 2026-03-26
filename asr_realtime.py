import sys
from dataclasses import dataclass

import numpy as np
import sounddevice as sd
from transformers import pipeline

from scoring import similarity_percent, label_score, normalize_text

# -----------------------
# Configuracion
# -----------------------
SAMPLE_RATE = 16000
SECONDS = 2.5
DEVICE = None

MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-spanish"

@dataclass
class RecorderConfig:
    sample_rate: int = SAMPLE_RATE
    seconds: float = SECONDS
    device: int | None = DEVICE

def grabar_audio(cfg: RecorderConfig) -> np.ndarray:
    print(f"Grabando {cfg.seconds:.1f}s... habla ahora")
    audio = sd.rec(
        int(cfg.seconds * cfg.sample_rate),
        samplerate=cfg.sample_rate,
        channels=1,
        dtype="float32",
        device=cfg.device
    )
    sd.wait()
    return audio.squeeze()

def normalizar(audio: np.ndarray) -> np.ndarray:
    peak = np.max(np.abs(audio)) if audio.size else 1.0
    if peak > 0:
        audio = audio / peak
    return audio

def main():
    print("Cargando modelo ASR...")
    asr = pipeline(
        "automatic-speech-recognition",
        model=MODEL_ID,
        device=-1,   # CPU
    )

    cfg = RecorderConfig()

    print("\nListo")
    print("▶ Presiona ENTER para grabar y transcribir.")
    print("▶ Escribe 'q' y ENTER para salir.\n")

    while True:
        cmd = input(">>> ").strip().lower()
        if cmd == "q":
            break

        # palabra esperada (opcional)
        expected = input("🎯 Palabra esperada (Enter para omitir): ").strip()

        audio = grabar_audio(cfg)
        audio = normalizar(audio)

        out = asr(audio, sampling_rate=cfg.sample_rate)
        text = out["text"].strip()

        print(f"\nTranscripción: {text}")

        if expected:
            score = similarity_percent(expected, text)
            verdict = label_score(score, ok=90.0, partial=70.0)
            print(f"Similitud: {score}% | Evaluación: {verdict}")
            print(f"   esperado:  {normalize_text(expected)}")
            print(f"   detectado: {normalize_text(text)}")

        print()

    print("Bye")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrumpido.")
        sys.exit(0)