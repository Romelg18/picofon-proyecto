# Picofon - Sistema de Evaluación de Pronunciación con IA

Picofon es un sistema basado en inteligencia artificial que permite convertir audio a texto y evaluar automáticamente la similitud entre una palabra esperada y la pronunciación del usuario.

Este proyecto está orientado a aplicaciones en:
- Educación 
- Entrenamiento de pronunciación
- Evaluaciones automatizadas
- Sistemas interactivos con reconocimiento de voz

---

## Funcionalidades

- Conversión de audio a texto (Speech-to-Text)  
- Procesamiento de archivos de audio en español  
- Evaluación de pronunciación mediante similitud  
- Sistema de pruebas automatizadas  
- Soporte para procesamiento en tiempo real  

---

## Tecnologías utilizadas

- Python  
- Modelos de reconocimiento de voz (ASR)  
- Wav2Vec2 (preentrenado en español)  
- Librerías de procesamiento de audio  

---

## Estructura del proyecto

picofon-proyecto/

├── audio/  
├── audio mp4/  
├── resultados/  
├── __pycache__/  

├── asr_es.py  
├── asr_realtime.py  
├── scoring.py  
├── run_tests.py  
├── lista_pruebas.txt  

---

## Instalación

1. Clonar el repositorio:

git clone https://github.com/Romelg18/picofon-proyecto.git  
cd picofon-proyecto  

2. Crear entorno virtual:

python -m venv venv  
venv\Scripts\activate  

3. Instalar dependencias:

pip install -r requirements.txt  

---

## ▶Uso

### 🔹 Transcripción de audio

python asr_es.py  

Resultado esperado:
- Conversión del audio a texto
- Salida en consola o archivo

---

### 🔹 Evaluación de pronunciación

python scoring.py  

El sistema compara:
- Palabra esperada
- Palabra reconocida

Y devuelve:
- Porcentaje de similitud

---

### 🔹 Ejecución de pruebas

python run_tests.py  

Permite validar múltiples audios automáticamente.

---

### 🔹 Modo tiempo real

python asr_realtime.py  

Permite capturar audio en vivo y procesarlo.

---

## Ejemplo de salida

Palabra esperada: hola  
Transcripción: ola  
Similitud: 85%  

---

## Lógica del sistema

1. Se ingresa un audio  
2. El modelo ASR lo convierte en texto  
3. Se compara con la palabra esperada  
4. Se calcula un porcentaje de similitud  
5. Se genera un resultado evaluable  

---


---

## Consideraciones

- La precisión depende de la calidad del audio  
- El modelo puede fallar con ruido o acentos fuertes  
- Se recomienda usar audios claros en formato `.wav`  
- Se recomienda usar el audio en tiempo real para futuras pruebas debido a que es el ultimo testeado y funciona correctamente
---



## Estado del proyecto

En desarrollo – versión inicial funcional  

---
