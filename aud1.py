from moviepy import VideoFileClip

def extract_audio_from_video(video_path = "vid.mp4", audio_path="aud.wav"):
    try:
        # Load the video file using VideoFileClip
        video_clip = VideoFileClip(video_path)
        
        # Check if the video clip has audio
        if video_clip.audio is None:
            print(f"Warning: The video file '{video_path}' does not contain any audio.")
            video_clip.close()  # Close the video clip to release resources
            return None # Exit the function
        
        # Extract the audio and save it to a file. Use .mp3 for compressed audio.
        video_clip.audio.write_audiofile(audio_path, codec='libmp3lame')
        print(f"Audio extracted and saved to {audio_path}")
        
        return video_clip.audio
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except OSError as e:
        print(f"OS error: {e}")
        # If it's related to ffmpeg, provide more detailed guidance
        if "ffmpeg" in str(e).lower():
            print("\nThis appears to be an ffmpeg-related error.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure resources are released (though VideoFileClip's context manager should handle this)
        if 'video_clip' in locals() and video_clip is not None:
            video_clip.close()

print(extract_audio_from_video("tempfile/vid.mp4", "tempfile/aud.wav"))