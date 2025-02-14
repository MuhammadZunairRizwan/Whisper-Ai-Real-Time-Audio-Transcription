import streamlit as st 
import sounddevice as sd
import numpy as np
import whisper
import queue
import sys
import os
st.set_page_config(page_title="Transcripto", layout="wide")
st.title("🎤 Real-Time Audio Transcription")
st.subheader("Using OpenAI Whisper for speech-to-text conversion")
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://media-private.canva.com/qxAIA/MAGe4KqxAIA/1/p.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJWF6QO3UH4PAAJ6Q%2F20250212%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250212T081624Z&X-Amz-Expires=20588&X-Amz-Signature=76f2b71d720f8998ae3dfd36b26bea925d1fab912703dc5680ba6dac628388a7&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Wed%2C%2012%20Feb%202025%2013%3A59%3A32%20GMT"); 
    }

    /* Optional: Change text color for visibility */
    [data-testid="stAppViewContainer"] * {
        color: rgb(255,255,255);  !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

            # Process audio in batches
            if len(audio_buffer) >= BUFFER_SIZE:
                audio_input = np.concatenate(audio_buffer)
                result = model.transcribe(audio_input, language="en")
                transcription+=" " + result["text"]
                placeholder.write(transcription)
                audio_buffer = []  # Clear the buffer

except KeyboardInterrupt:
    print("Stopping transcription...")

# Clean up
stream.stop()
stream.close()


