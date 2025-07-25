from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torchaudio
from model.utils import load_model, predict, create_carnatic_filterbank, extract_carnatic_features_from_waveform
import os
import torch
import numpy as np
from pydub import AudioSegment
import io

app = FastAPI() #this starts the instance.

# Enable CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) #Cors is the gatekeeping security mechanism. You have to give whats alllowed, or everything is blocked 

# Load model, class names, and create filterbank once
filterbank = create_carnatic_filterbank()
model, class_names = load_model("model/best_model.pth", "model/class_names.json")

@app.post("/predict/") #when the user goes to /predict, the predict_audio is called.
#post means that "I'm giving u this. do something with it and RETURN something"
#get means that " give me xyz data"
#put is used to update stuff.

async def predict_audio(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename.lower()

    # Save uploaded file temporarily as temp_input
    with open("temp_input", "wb") as f:
        f.write(contents)

    # Always use pydub to convert to 22050 Hz wav and truncate to 30s
    audio = AudioSegment.from_file("temp_input")
    audio = audio.set_frame_rate(22050).set_channels(1)
    audio = audio[:30_000]  # Truncate to first 30 seconds (30,000 ms)
    audio.export("temp.wav", format="wav")
    os.remove("temp_input")  # Clean up the input file

    waveform, sample_rate = torchaudio.load("temp.wav")

    features = extract_carnatic_features_from_waveform(waveform, sample_rate, filterbank)
    feature_tensor = torch.tensor(features, dtype=torch.float32)

    prediction = predict(model, class_names, feature_tensor)
    os.remove("temp.wav")

    return {"prediction": prediction}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
