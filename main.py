#!/bin/python
import azure.cognitiveservices.speech as speechsdk
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
from asyncio import Queue
import datetime

app = FastAPI()

# Azure Speech SDK Configuration
speech_key = "YOUR-AZURE-SPEECH-KEY"
service_region = "YOUR-SERVICE-REGION"
# Create a speech config instance
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

@app.get("/")
async def root():
    return {"message": "WebSocket server is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established")

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    queue = Queue()
    transcription = []  # List to store recognized text for writing to file

   

    

    # Speech recognition event handling
    def recognize_callback(evt):
        recognized_text = evt.result.text
        if recognized_text:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_text = f"[{timestamp}] {recognized_text}"
            print(f"Recognized: {formatted_text}")
            queue.put_nowait(formatted_text)  # Send recognized text to queue
            transcription.append(formatted_text)  # Add recognized text to transcription list

    recognizer.recognized.connect(recognize_callback)
    recognizer.start_continuous_recognition()  # Start recognition session

    try:
        while True:
            # Wait for and send recognized text to WebSocket
            result_text = await queue.get()
            await websocket.send_text(result_text)

    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        # Stop recognition and close WebSocket
        recognizer.stop_continuous_recognition()
        await websocket.close()

        # Write transcription to a file
        file_path = "audio_transcription.txt"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(transcription))
            print(f"Transcription saved to {file_path}")
