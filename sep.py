import os
import torch
from demucs.pretrained import get_model
from demucs.audio import AudioFile, save_audio
from demucs.apply import apply_model

def separate_audio(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Load model (htdemucs is the latest model with good separation quality)
    model = get_model("htdemucs")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    # Load audio file
    wav = AudioFile(input_file).read(streams=0, samplerate=model.samplerate, channels=model.audio_channels)
    ref = wav.mean(0)
    wav = (wav - ref.mean()) / ref.std()
    
    # Apply separation - use apply_model instead of model.forward
    with torch.no_grad():
        sources = apply_model(model, wav[None], device=device)
    sources = sources * ref.std() + ref.mean()
    
    # Save each source in output directory
    track_name = os.path.splitext(os.path.basename(input_file))[0]
    track_dir = output_dir
    os.makedirs(track_dir, exist_ok=True)
    
    # Get the index of vocals from the model sources
    sources_list = model.sources
    vocals_idx = sources_list.index('vocals')
    
    # Save vocals track
    vocals = sources[0][vocals_idx]
    vocals_path = os.path.join(track_dir, "vocals.wav")
    save_audio(vocals, vocals_path, model.samplerate)
    
    # Create and save music track (everything except vocals)
    # Start with zeros, then add all non-vocal sources
    music = torch.zeros_like(vocals)
    for i, source_name in enumerate(sources_list):
        if source_name != 'vocals':
            music += sources[0][i]
    
    music_path = os.path.join(track_dir, "music.wav")
    save_audio(music, music_path, model.samplerate)
    
    print(f"Separation complete! Files saved to {track_dir}")
    
    
separate_audio("tempfile/aud.wav", "tempfile/aud")