# Transcripto - Real-Time Audio Transcription
## Overview
Whisper-Ai is a real-time speech-to-text transcription application powered by **OpenAI Whisper** and **Streamlit**. This application captures live audio input, processes it using Whisper, and displays the transcribed text in real time.

## Features
- 🎤 **Live Audio Transcription** using OpenAI Whisper
- 📡 **Real-Time Processing** with Streamlit
- 🎨 **Custom Background Styling** for an enhanced UI experience
- 🎛 **Adjustable Audio Parameters** for flexible performance tuning

## Requirements
### Dependencies
- Python 3.8+
- `streamlit`
- `sounddevice`
- `numpy`
- `whisper`
- `queue`

Install them using:
```sh
pip install streamlit sounddevice numpy openai-whisper
```

## How to Run
### Clone the repository
```sh
git clone https://github.com/yourusername/whisper-ai.git
cd whisper-ai
```

### Run the application
```sh
streamlit run app.py
```

## Configuration
### Modify Audio Parameters
The script captures audio using **sounddevice** with the following parameters:
- `SAMPLE_RATE = 16000`  # Adjust sample rate if needed
- `CHUNK_SIZE = 4096`  # Defines processing chunk size
- `INPUT_DEVICE = 5`  # Change based on available devices

To find the correct input device ID, run:
```sh
python -c "import sounddevice as sd; print(sd.query_devices())"
```
Update `INPUT_DEVICE` accordingly.

## Troubleshooting
### Common Issues & Fixes
- If you encounter **no matching device errors**, try manually specifying the input device ID.
- Ensure **Whisper** is installed properly with `pip install openai-whisper`.
- If Streamlit does not load, try updating it:
```sh
pip install --upgrade streamlit
```




