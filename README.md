# DubAI: AI Video Dubbing System

## Introduction
In an increasingly globalized world, the demand for multilingual video content is growing rapidly. **DubAI** is an automated video dubbing system designed to simplify the process of creating dubbed versions of YouTube videos in different languages. By leveraging state-of-the-art AI models and libraries for transcription, translation, and text-to-speech synthesis, DubAI automates the entire dubbing pipeline, making it accessible to content creators, educators, and businesses.

> **Key Features:**
> - Automated transcription and translation.
> - High-quality audio separation and dubbing.
> - Seamless integration of dubbed audio with video.

---

## Project Overview
DubAI takes a YouTube video link and a target language as input. It processes the video to:

1. Extract audio from the video.
2. Separate vocals and background music.
3. Transcribe the vocals into text with timestamps.
4. Translate the transcription into the target language.
5. Generate dubbed audio using text-to-speech synthesis.
6. Merge the dubbed audio with the background music.
7. Add the combined audio back to the original video.

The final output is a fully dubbed video in the desired language.

---

## Libraries and Tools Used

### 1. Video and Audio Processing
- **[MoviePy](https://zulko.github.io/moviepy/):** Used for video and audio manipulation, including extracting audio from video files and adding audio back to videos. MoviePy provides a high-level API for handling multimedia files.
- **[Pydub](https://github.com/jiaaro/pydub):** Used for audio processing tasks such as adjusting audio duration and merging audio tracks. It simplifies working with audio formats like WAV and MP3.
- **[FFmpeg](https://www.ffmpeg.org/):** A powerful multimedia framework used for encoding, decoding, and processing audio and video files. It is required by MoviePy for handling media files.

### 2. YouTube Video Download
- **[Pytubefix](https://github.com/JuanBindez/pytubefix):** A library for downloading YouTube videos. It supports fetching the highest resolution video streams and provides callbacks for monitoring download progress.

### 3. Audio Separation
- **[Demucs](https://github.com/facebookresearch/demucs):** A deep learning-based model for audio source separation. It is used to separate vocals and background music from the extracted audio. The `htdemucs` model, known for its high-quality separation, is employed in this project.

### 4. Speech-to-Text Transcription
- **[OpenAI Whisper](https://github.com/openai/whisper):** A state-of-the-art speech recognition model capable of transcribing audio into text with word-level timestamps. Whisper supports multiple languages and provides robust transcription even in noisy environments.

### 5. Translation
- **[Google Generative AI (Gemini)](https://ai.google/):** Used for translating the transcribed text into the target language. The Gemini model ensures accurate translations while preserving the tone and meaning of the original text.

### 6. Text-to-Speech Synthesis
- **[gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/):** A Python library for converting text into speech. It supports multiple languages and is used to generate dubbed audio from the translated text.

---

## Technical Workflow

### Step 1: Download the YouTube Video
The `pytubefix` library is used to download the YouTube video. The highest resolution stream is fetched and saved to a temporary directory for further processing.

```python
from pytubefix import YouTube

def video_download(url):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    ys.download(output_path="/tempfile/")
```

### Step 2: Extract Audio from Video
The `MoviePy` library is used to extract audio from the downloaded video. The extracted audio is saved as a WAV file for further processing.

```python
from moviepy.video.io.VideoFileClip import VideoFileClip

def extract_audio_from_video(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    video_clip.audio.write_audiofile(audio_path, codec='libmp3lame')
```

### Step 3: Separate Vocals and Background Music
The `Demucs` model is used to separate the audio into vocals and background music. This step is crucial for accurate transcription and dubbing.

```python
from demucs.pretrained import get_model
from demucs.apply import apply_model

def separate_audio(input_file, output_dir):
    model = get_model("htdemucs")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    # Apply the model to separate vocals and music
```

### Step 4: Transcribe Audio to Text
The `OpenAI Whisper` model is used to transcribe the vocal audio into text. The transcription includes word-level timestamps for precise synchronization.

```python
import whisper

def transcribe_with_local_whisper(audio_file, model_size="small"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_file, word_timestamps=True)
    return result["segments"]
```

### Step 5: Translate the Transcription
The transcription is translated into the target language using the `Google Generative AI (Gemini)` model. The translation retains the original meaning and tone.

```python
import google.generativeai as genai

def translate_text(text, target_language, model):
    prompt = f"Translate the following text to {target_language}: {text}"
    response = model.generate_content(prompt)
    return response.text
```

### Step 6: Generate Dubbed Audio
The translated text is converted into speech using the `gTTS` library. The generated audio is synchronized with the original timestamps.

```python
from gtts import gTTS

def text_to_speech(text, lang, output_file):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
```

### Step 7: Merge Audio Tracks
The dubbed audio is merged with the background music using `MoviePy`. The combined audio is then added back to the original video.

```python
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip

def merge_audio_tracks(dubbed_audio_path, music_path, output_audio_path):
    dubbed_audio = AudioFileClip(dubbed_audio_path)
    music_audio = AudioFileClip(music_path)
    combined_audio = CompositeAudioClip([dubbed_audio, music_audio])
    combined_audio.write_audiofile(output_audio_path, codec='aac')
```

### Step 8: Add Audio to Video
The combined audio is added to the original video to create the final dubbed video.

```python
from moviepy.video.io.VideoFileClip import VideoFileClip

def add_audio_to_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path).without_audio()
    audio_clip = AudioFileClip(audio_path)
    video_clip.audio = audio_clip
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
```

---

## Conclusion
DubAI demonstrates the power of combining advanced AI models and libraries to automate complex tasks like video dubbing. By leveraging tools like Whisper, Demucs, and Google Generative AI, DubAI achieves high-quality results with minimal manual intervention. This project serves as a robust foundation for creating multilingual video content and can be extended to support additional languages and features.

