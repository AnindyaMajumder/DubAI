import yt_download
import aud
import sep
import transcribe
import translate
import dubbed
import merge_aud

def get_language_code(language):
    # You can expand this mapping as needed
    mapping = {
        "hindi": "hi",
        "english": "en",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "bengali": "bn",
        "tamil": "ta",
        "telugu": "te",
        "japanese": "ja",
        "korean": "ko",
        "chinese": "zh",
        "marathi": "mr",
        "gujarati": "gu",
        "punjabi": "pa",
        "urdu": "ur",
        "russian": "ru",
        "portuguese": "pt",
        "italian": "it",
        "turkish": "tr",
        "arabic": "ar",
        "thai": "th",
        "malayalam": "ml",
        "kannada": "kn",
        "oriya": "or",
        "assamese": "as",
        "nepali": "ne",
        "sinhala": "si",
        "burmese": "my",
        "khmer": "km",
        "vietnamese": "vi",
        "indonesian": "id",
        "swahili": "sw",
        "filipino": "tl",
    }
    return mapping.get(language.lower(), language)

if __name__ == "__main__":
    # 🎥 Step 0: Download the YouTube Video
    print("📥 Enter the URL of the YouTube video to download:")
    yt_download.video_download(input())
    print("🌍 Enter the target language for translation:")
    translation_lan = input().lower()
    print("\n\n")

    # 🎵 Step 1: Extract Audio from Video
    print("🎞️ Extracting audio from video...")
    aud.extract_audio_from_video("tempfile/vid.mp4", "tempfile/aud.wav")
    print("✅ Audio extracted successfully!\n")

    # 🎤 Step 2: Separate Vocals and Music
    print("🎧 Wait a little longer... Audio separation in progress...")
    sep.separate_audio("tempfile/aud.wav", "tempfile/aud")
    print("✅ Audio separation complete!\n")

    # 📝 Step 3: Transcribe Audio to Text
    print("📝 Transcribing vocals...")
    audio_file = "tempfile/aud/vocals.wav"
    output_file = "tempfile/transcription.txt"
    segments = transcribe.transcribe_with_local_whisper(audio_file, "medium")
    transcribe.save_transcription(segments, output_file)
    print(f"✅ Transcription complete: {audio_file} → {output_file}\n")

    # 🌐 Step 4: Translate Transcription
    translate.translate_transcript("tempfile/transcription.txt", translation_lan)
    print("✅ Translation complete!\n")

    # 🗣️ Step 5: Generate Dubbed Audio with Translation
    print("🔊 Generating dubbed audio with translated text...")
    input_file = f"tempfile/transcription_{translation_lan.replace(' ', '_')}.txt"
    language = get_language_code(translation_lan)
    temp_directory = "tempfile/dubbed_temp"
    final_output = "tempfile/complete_dubbed.mp3"
    dubbed.dub_text_with_timestamps(input_file, language, temp_directory, final_output)
    print("✅ Dubbed audio generation complete!\n")

    # 🎬 Step 6: Merge Audio Tracks and Add to Video
    print("🎵 Merging dubbed audio and background music...")
    video_path = "tempfile/vid.mp4"
    dubbed_audio_path = "tempfile/complete_dubbed.mp3"
    music_path = "tempfile/aud/music.wav"
    combined_audio_path = "tempfile/temp-audio.m4a"
    output_video_path = "output.mp4"
    merged_audio = merge_aud.merge_audio_tracks(dubbed_audio_path, music_path, combined_audio_path)
    if merged_audio:
        print("🎥 Adding merged audio to the video...")
        merge_aud.add_audio_to_video(video_path, merged_audio, output_video_path)
        print(f"✅ Video with dubbed audio created successfully: {output_video_path}\n")
    else:
        print("❌ Failed to merge audio tracks!\n")