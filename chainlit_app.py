#!/bin/python

import chainlit as cl
import websockets
import asyncio

# Connect to WebSocket FastAPI server
SERVER_URI = "ws://127.0.0.1:8000/ws"



# Handle messages as they come in
@cl.on_message
async def on_message(msg):
    async with websockets.connect(SERVER_URI) as websocket:
        await websocket.send("start")  # Initialize speech recognition stream
        await cl.Message(content="Connected to live audio transcription!").send()

        # Handle live transcription stream
        while True:
            try:
                response = await websocket.recv()  # Receive transcription text
                await cl.Message(content=f"Transcription: {response}", author="System").send()
            except Exception as e:
                await cl.Message(content=f"Error receiving transcription: {str(e)}", author="Error").send()
                break
