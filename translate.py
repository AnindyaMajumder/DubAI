import re
import google.generativeai as genai
import os
from dotenv import load_dotenv

def parse_transcript(transcript_file):
    """
    Format: [start_time - end_time] text
    """
    segments = []
    with open(transcript_file, 'r') as file:
        for line in file:
            # Skip empty lines or file path comments
            if not line.strip() or line.strip().startswith('//'):
                continue
                
            # Parse timestamp and text
            match = re.match(r'\[([\d.]+) - ([\d.]+)\]\s+(.*)', line)
            if match:
                start_time = float(match.group(1))
                end_time = float(match.group(2))
                text = match.group(3).strip()
                segments.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'text': text
                })
    
    return segments

def translate_text(text, target_language, model):
    prompt = f"Translate the following English text to {target_language}. Keep the same meaning, tone and spoken style:\n\n{text}.\n\nOnly return the translated text, no options or any other text needed."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

def translate_transcript(transcript_file, target_language):
    """
    Translate a transcript file to the specified language and save the result
    """
    # Load environment variables for API keys
    load_dotenv()
    
    # Configure Gemini AI
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        return
    
    # Parse the transcript
    segments = parse_transcript(transcript_file)
    if not segments:
        print(f"No valid segments found in {transcript_file}")
        return
    
    # Translate each segment
    translated_segments = []
    for i, segment in enumerate(segments):
        translated_text = translate_text(segment['text'], target_language, model)
        translated_segments.append({
            'start_time': segment['start_time'],
            'end_time': segment['end_time'],
            'text': translated_text
        })
    
    # Generate output filename
    base_name = os.path.splitext(transcript_file)[0]
    output_file = f"{base_name}_{target_language.lower().replace(' ', '_')}.txt"
    
    # Write translated transcript
    with open(output_file, 'w') as file:
        for segment in translated_segments:
            file.write(f"[{segment['start_time']:.2f} - {segment['end_time']:.2f}]  {segment['text']}\n")
    
    print(f"Translation complete. Output saved to {output_file}")

    
translate_transcript("tempfile/transcription.txt", input("Enter the target language: "))