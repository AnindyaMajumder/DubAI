import re
import os
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment

def parse_timestamped_text(file_path):
    """
    Parse a file containing timestamped text segments.
    Expected format: [start_time - end_time] text
    Returns a list of (start_time, end_time, text) tuples.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regular expression to match timestamps and text
    pattern = r'\[([\d.]+) - ([\d.]+)\]\s+(.*?)(?=\n\[|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    result = []
    for start_time, end_time, text in matches:
        result.append((float(start_time), float(end_time), text.strip()))
    
    return result

def text_to_speech(text, lang, output_file):
    """Generate speech from text and save to file"""
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_file)
    return output_file

def adjust_audio_duration(audio_segment, target_duration_ms):
    """
    Adjust audio segment to match target duration by speeding up/slowing down
    without changing pitch.
    """
    current_duration_ms = len(audio_segment)
    
    if current_duration_ms == 0:
        return AudioSegment.silent(duration=target_duration_ms)
    
    # Calculate the necessary speed factor
    speed_factor = current_duration_ms / target_duration_ms
    
    if abs(speed_factor - 1.0) < 0.05:  # If difference is less than 5%
        return audio_segment
    
    # Limit speed adjustment to reasonable bounds
    speed_factor = max(0.5, min(2.0, speed_factor))
    
    # Apply speed change
    adjusted_audio = audio_segment.speedup(playback_speed=speed_factor)
    
    # If still not exact, trim or pad
    final_duration = len(adjusted_audio)
    if final_duration > target_duration_ms:
        # Trim end
        adjusted_audio = adjusted_audio[:target_duration_ms]
    elif final_duration < target_duration_ms:
        # Pad with silence
        silence_ms = target_duration_ms - final_duration
        adjusted_audio = adjusted_audio + AudioSegment.silent(duration=silence_ms)
    
    return adjusted_audio

def dub_text_with_timestamps(input_file, lang, output_dir, final_output):
    """
    Main function to dub text segments according to timestamps and merge them.
    Ensures output audio maintains original timestamps.
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Parse the timestamped text
    segments = parse_timestamped_text(input_file)
    print(f"Found {len(segments)} text segments to process")
    
    # Create a blank audio file that will hold our final output
    final_audio = AudioSegment.silent(duration=0)
    last_end_time = 0
    
    # Process each segment
    for i, (start_time, end_time, text) in enumerate(segments):
        # Generate output filename for this segment
        segment_file = os.path.join(output_dir, f"segment_{i+1:03d}.mp3")
        
        # Convert text to speech
        text_to_speech(text, lang, segment_file)
        
        # Load the generated speech
        speech = AudioSegment.from_mp3(segment_file)
        
        # Calculate desired duration in milliseconds
        target_duration_ms = int((end_time - start_time) * 1000)
        
        # Adjust speech to match target duration
        adjusted_speech = adjust_audio_duration(speech, target_duration_ms)
        
        # Add silence gap if needed
        silence_duration_ms = int((start_time - last_end_time) * 1000)
        if silence_duration_ms > 0:
            final_audio += AudioSegment.silent(duration=silence_duration_ms)
        
        # Add the adjusted speech
        final_audio += adjusted_speech
        
        # Update last_end_time
        last_end_time = end_time
        
        print(f"Added segment with duration: {target_duration_ms/1000:.2f} seconds")
    
    # Export the final audio
    print(f"\nExporting final audio to {final_output}...")
    final_audio.export(final_output, format="mp3")
    print(f"Successfully created audio file: {final_output}")
    print(f"Total duration: {len(final_audio)/1000:.2f} seconds")
    
    return final_output

# Hardcoded values
input_file = "tempfile/transcription_spanish.txt"
language = "es"  
temp_directory = "tempfile/dubbed_temp"
final_output = "tempfile/complete_dubbed.mp3"

# Execute the function with hardcoded values
dub_text_with_timestamps(input_file, language, temp_directory, final_output)