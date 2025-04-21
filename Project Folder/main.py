import yt_download
import aud
import sep
import transcribe
import translate
import dubbed
import merge_aud

if __name__ == "__main__":
    print("=== DubAI Automated Video Dubbing Pipeline ===\n")

    # 1. Download YouTube video
    url = input("Enter the URL of the YouTube video: ")
    yt_download.video_download(url)
    video_path = "tempfile/vid.mp4"

    # 2. Extract audio from video
    print("\nExtracting audio from video...")
    audio_path = "tempfile/aud.wav"
    aud.extract_audio_from_video(video_path, audio_path)

    # 3. Separate vocals and music
    print("\nSeparating vocals and music...")
    sep.separate_audio(audio_path, "tempfile/aud")
    vocals_path = "tempfile/aud/vocals.wav"
    music_path = "tempfile/aud/music.wav"

    # 4. Transcribe vocals
    print("\nTranscribing vocals...")
    transcription_path = "tempfile/transcription.txt"
    transcribe.segments = transcribe.transcribe_with_local_whisper(vocals_path, model_size="small")
    transcribe.save_transcription(transcribe.segments, transcription_path)

    # 5. Translate transcript
    print("\nTranslating transcript...")
    target_language = input("Enter the target language: ")
    translate.translate_transcript(transcription_path, target_language)
    translated_transcript_path = f"tempfile/transcription_{target_language.lower().replace(' ', '_')}.txt"

    # 6. Generate dubbed audio
    print("\nGenerating dubbed audio...")
    dubbed_output_dir = "tempfile/dubbed_temp"
    dubbed_final_output = "tempfile/complete_dubbed.mp3"
    dubbed.dub_text_with_timestamps(translated_transcript_path, target_language, dubbed_output_dir, dubbed_final_output)

    # 7. Merge dubbed audio with background music
    print("\nMerging dubbed audio with background music...")
    combined_audio_path = "tempfile/temp-audio.m4a"
    merge_aud.merge_audio_tracks(dubbed_final_output, music_path, combined_audio_path)

    # 8. Add merged audio to video
    print("\nAdding merged audio to video...")
    output_video_path = "output.mp4"
    merge_aud.add_audio_to_video(video_path, combined_audio_path, output_video_path)

    print("\n=== Pipeline Complete! Output saved as output.mp4 ===")