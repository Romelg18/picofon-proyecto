import sys
import torch
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

MODEL_NAME = "jonatasgrosman/wav2vec2-large-xlsr-53-spanish"

#  Cargar modelo y processor UNA sola vez (más rápido)
processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_NAME)
model.eval()

def transcribe(path_wav: str) -> str:
    # 1) Cargar audio y forzar a 16kHz mono (requisito para wav2vec2)
    audio, sr = librosa.load(path_wav, sr=16000, mono=True)

    # 2) Convertir audio a tensores
    inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)

    # 3) Inferencia (sin gradientes)
    with torch.no_grad():
        logits = model(inputs.input_values).logits

    # 4) Elegir la clase más probable por frame y decodificar
    pred_ids = torch.argmax(logits, dim=-1)
    text = processor.batch_decode(pred_ids)[0]
    return text.lower().strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python asr_es.py <ruta_audio.wav>")
        print("Ejemplo: python asr_es.py audio\\peyu.wav")
        sys.exit(1)

    path = sys.argv[1]

    print("Transcripción:")
    print(transcribe(path))
