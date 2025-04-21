import json
import os
import wave
from typing import Dict, List, Tuple
import numpy as np
import torch
import whisper

def read_wav_file(file_path: str) -> Tuple[np.ndarray, int]:
    """Read a WAV file and return audio data and sample rate"""
    with wave.open(file_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        audio_data = np.frombuffer(wf.readframes(frames), dtype=np.int16).astype(np.float32) / 32768.0
        return audio_data, rate

def transcribe_with_local_whisper(audio_file: str, model_size: str = "small") -> List[Dict]:
    """Transcribe audio using local Whisper model with timestamps"""
    print(f"Transcribing {audio_file} with Whisper {model_size} model...")
    
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load the Whisper model
    model = whisper.load_model(model_size, device=device)
    
    # Transcribe the audio
    print("Running transcription...")
    result = model.transcribe(
        audio_file, 
        verbose=True,   # Show progress
        word_timestamps=True  # Enable word-level timestamps
    )
    
    # Format segments to match our expected structure
    segments = []
    for segment in result.get("segments", []):
        segments.append({
            "text": segment["text"],
            "timestamp": [segment["start"], segment["end"]]
        })
    
    # If no segments are returned, fall back to full text
    if not segments and "text" in result:
        segments.append({
            "text": result["text"],
            "timestamp": [0.0, 30.0]
        })
    
    return segments

def save_transcription(segments: List[Dict], output_file: str):
    """Save transcription with timestamps to file"""
    file_extension = os.path.splitext(output_file)[1].lower()
    
    if file_extension == '.json':
        with open(output_file, 'w') as f:
            json.dump(segments, f, indent=2)
    elif file_extension == '.txt':
        with open(output_file, 'w') as f:
            for segment in segments:
                start = segment['timestamp'][0]
                end = segment['timestamp'][1]
                text = segment['text']
                # Add four spaces after timestamp to match your desired format
                f.write(f"[{start:.2f} - {end:.2f}]    {text}\n")
    else:
        raise ValueError("Unsupported file extension. Use .json or .txt")
    
    print(f"Transcription saved to {output_file}")

# if __name__ == "__main__":
#     audio_file = "tempfile/aud/vocals.wav"
#     output_file = "tempfile/transcription.txt"
    
#     # Choose model size: 'tiny', 'base', 'small', 'medium', or 'large'
#     model_size = "small"  # Smaller models are faster but less accurate
    
#     # Run transcription using local Whisper
#     segments = transcribe_with_local_whisper(audio_file, model_size)
#     save_transcription(segments, output_file)
#     print(f"Transcription complete: {audio_file} → {output_file}")