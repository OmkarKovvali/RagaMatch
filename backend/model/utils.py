import json
import torch
import numpy as np
import librosa
import sys
import os

# Add the current directory to the path to handle imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from my_model import RagaTDNNLSTMAttention

def create_carnatic_filterbank(sr=22050, n_fft=2048):
    swara_freqs = np.linspace(61, 1319, 58)
    filterbank = []
    freq_bins = np.linspace(0, sr/2, n_fft//2+1)
    for i in range(1, len(swara_freqs)-1):
        f_left = swara_freqs[i-1]
        f_center = swara_freqs[i]
        f_right = swara_freqs[i+1]
        response = np.zeros_like(freq_bins)
        left_mask = (freq_bins >= f_left) & (freq_bins <= f_center)
        right_mask = (freq_bins >= f_center) & (freq_bins <= f_right)
        response[left_mask] = (freq_bins[left_mask] - f_left) / (f_center - f_left)
        response[right_mask] = (f_right - freq_bins[right_mask]) / (f_right - f_center)
        filterbank.append(response)
    return np.array(filterbank)

def extract_carnatic_features_from_waveform(waveform, sample_rate, filterbank, n_fft=2048, hop_length=512, max_len=1300):
    y = waveform.squeeze().numpy()
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))**2
    features = np.dot(filterbank, S)
    features = features / (np.mean(features, axis=0, keepdims=True) + 1e-8)
    log_features = librosa.power_to_db(features, ref=np.max)
    if log_features.shape[1] < max_len:
        pad_width = max_len - log_features.shape[1]
        log_features = np.pad(log_features, ((0,0),(0,pad_width)), mode='constant')
    else:
        log_features = log_features[:, :max_len]
    
    if log_features.shape[0] != 56:
        raise ValueError(f"Expected 56 filter channels, got {log_features.shape[0]}")
    print(f"[extract] shape: {log_features.shape}, mean: {np.mean(log_features):.2f}, std: {np.std(log_features):.2f}")
    return log_features

def load_model(model_path:str, class_names_path:str):
    input_size = 56
    time_steps = 1300
    
    # Load class names first to determine number of classes
    with open(class_names_path,'r') as f:
        class_names = json.load(f)
    
    num_classes = len(class_names)
    print(f"Loading model with {num_classes} classes")
    
    model = RagaTDNNLSTMAttention(input_size=input_size, time_steps=time_steps, num_classes=num_classes)
    state_dict = torch.load(model_path, map_location=torch.device('cpu'))
    model.load_state_dict(state_dict)
    model.eval() # sets the Neural network to evaluation mode. Dropout layers are disabled
    # Batch Normalization is also tweaked a bit
    return model, class_names

#def predict(model, class_names, audio_tensor):
    #with torch.no_grad(): #says to not build a computation graph here. still works without this, but memory wasted
        # "with" is a context manager. Works like below
        # "with open("file.txt") as f:" is the same as 
        #f = open("file.txt")
        #try:
        # do stuff with f
        #finally:
        #f.close()  # cleanup happens automatically
        #output = model(audio_tensor.unsqueeze(0))
        #prediction = torch.argmax(output,dim=1).item()
        #the return just simply uses dict properties to check for where the actual labelled prediction is
        #return class_names[prediction]
    
def predict(model, class_names, audio_tensor):
    with torch.no_grad():
        output = model(audio_tensor.unsqueeze(0))
        prediction = torch.argmax(output, dim=1).item()
        if class_names[0] == ".zip":
            prediction -= 1
            return class_names[prediction + 1]  # correct offset
        return class_names[prediction]

