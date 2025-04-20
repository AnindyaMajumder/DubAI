from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

def merge_audio_tracks(dubbed_audio_path, music_path, output_audio_path):
    """
    Merge dubbed audio and background music into a single audio file.
    
    Args:
        dubbed_audio_path (str): Path to the main dubbed audio
        music_path (str): Path to the background music
        output_audio_path (str): Path for the output combined audio file
    """
    try:
        # Load audio clips
        dubbed_audio = AudioFileClip(dubbed_audio_path)
        music_audio = AudioFileClip(music_path)
        
        # Combine the audio tracks
        combined_audio = CompositeAudioClip([dubbed_audio, music_audio])
        
        # Write the combined audio to file
        combined_audio.write_audiofile(output_audio_path, codec='aac')
        
        # Close clips to free resources
        dubbed_audio.close()
        music_audio.close()
        combined_audio.close()
        
        print(f"Successfully merged audio tracks to {output_audio_path}")
        return output_audio_path
        
    except Exception as e:
        print(f"Error merging audio tracks: {e}")
        return None

def add_audio_to_video(video_path, audio_path, output_path):
    """
    Add audio to a muted video.
    
    Args:
        video_path (str): Path to the video file
        audio_path (str): Path to the audio file
        output_path (str): Path for the output video file
    """
    try:
        # Load video clip and mute it
        video_clip = VideoFileClip(video_path)
        muted_video = video_clip.without_audio()
        
        # Load the combined audio
        audio_clip = AudioFileClip(audio_path)
        
        # Set the audio to the muted video
        final_video = muted_video
        final_video.audio = audio_clip
        
        # Write the result to file with proper codecs
        final_video.write_videofile(output_path, 
                                   codec='libx264',
                                   audio_codec='aac', 
                                   temp_audiofile="temp-audio.m4a", 
                                   remove_temp=True)
        
        # Close all clips
        video_clip.close()
        muted_video.close()
        audio_clip.close()
        final_video.close()
        
        print(f"Successfully added audio to video at {output_path}")
        
    except Exception as e:
        print(f"Error adding audio to video: {e}")

if __name__ == "__main__":
    # Paths for the input files
    video_path = "tempfile/vid.mp4"
    dubbed_audio_path = "tempfile/complete_dubbed.mp3"
    music_path = "tempfile/aud/music.wav"
    
    # Output paths
    combined_audio_path = "tempfile/temp-audio.m4a"
    output_video_path = "output.mp4"
    
    # Step 1 & 2: Merge the audio files
    merged_audio = merge_audio_tracks(dubbed_audio_path, music_path, combined_audio_path)
    
    # Step 3: Add the combined audio to the muted video
    if merged_audio:
        add_audio_to_video(video_path, merged_audio, output_video_path)