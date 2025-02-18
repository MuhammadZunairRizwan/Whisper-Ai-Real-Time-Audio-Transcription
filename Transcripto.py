import streamlit as st 
import sounddevice as sd
import numpy as np
import whisper
import queue
import sys
import os
import base64

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "cover.jpg")
def get_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
base64_image = get_base64(image_path)
st.set_page_config(page_title="Transcripto", layout="wide")
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stAppViewContainer"] {{
        color: rgb(255,255,255);  !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎤 Real-Time Audio Transcription")
st.subheader("Using OpenAI Whisper for speech-to-text conversion")
st.write("Transcription")
model = whisper.load_model("base")

# Audio parameters
SAMPLE_RATE = 16000  
CHUNK_SIZE = 4096  
INPUT_DEVICE = 5  

# Queue to hold audio data
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """Callback function to capture audio data."""
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(indata.copy())

# Start capturing system audio
print("Starting system audio capture...")
stream = sd.InputStream(
    device=INPUT_DEVICE,  
    samplerate=SAMPLE_RATE,
    channels=1,  
    dtype=np.float32,
    callback=audio_callback,
    blocksize=CHUNK_SIZE
)

stream.start()

print("Real-time transcription started. Press Ctrl+C to stop...")
transcription=" "
# Buffer to collect audio chunks
audio_buffer = []
BUFFER_SIZE = 5   
placeholder=st.empty()
try:
    while True:
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            audio_buffer.append(audio_data.flatten())

           
            if len(audio_buffer) >= BUFFER_SIZE:
                audio_input = np.concatenate(audio_buffer)
                result = model.transcribe(audio_input, language="en")
                transcription+=" " + result["text"]
                placeholder.write(transcription)
                audio_buffer = [] 

except KeyboardInterrupt:
    print("Stopping transcription...")


stream.stop()
stream.close()


