Azure Speech SDK Configuration is needed to run the code.
The user needs to manually edit the speech key and service region variables in the main.py file.
Here is an example below:
```
speech_key = "YOUR-AZURE-SPEECH-KEY"
service_region = "YOUR-SERVICE-REGION"
```
Installation:
```
pip install chainlit fastapi websockets asyncio azure-cognitiveservices-speech
```
Instructions:

Run FastAPI Server first terminal
```
>> python -m uvicorn main:app --reload
```
Run Chainlit Interface second terminal
```
>> python -m chainlit run chainlit_app.py -w --port 8500
```
After stop recording and end the websocket session, the transcription will be save as
```audio_transcription.txt```




