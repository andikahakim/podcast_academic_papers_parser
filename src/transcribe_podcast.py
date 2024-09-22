# src/transcribe_podcast.py
import whisper
import json
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import os
import sys
import torch
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
warnings.filterwarnings("ignore", category=FutureWarning, message="You are using `torch.load` with `weights_only=False`")

def transcribe_audio(file_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("small", device=device)
    result = model.transcribe(file_path)
    return result['text'], result['segments']

def transcribe_youtube(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript]), transcript
    except Exception as e:
        print(f"Error fetching YouTube transcript: {e}")
        return None, None

def download_youtube_audio(video_url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, 'temp_audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return os.path.join(output_path, 'temp_audio.mp3')

def process_input(input_data, output_path):
    if input_data.startswith("http"):
        video_id = input_data.split("v=")[-1]
        transcript, segments = transcribe_youtube(video_id)
        if not transcript:
            audio_file = download_youtube_audio(input_data, output_path)
            if audio_file:
                transcript, segments = transcribe_audio(audio_file)
                os.remove(audio_file)
            else:
                print("Failed to download audio from YouTube.")
                return
        source = "YouTube"
        title = input_data
        output_file_name = f"{video_id}.json"
    else:
        transcript, segments = transcribe_audio(input_data)
        source = "Audio File"
        title = os.path.basename(input_data)
        output_file_name = f"{os.path.splitext(title)[0]}.json"
    
    metadata = {
        "title": title,
        "source": source,
        "content": transcript,
        "segments": segments
    }
    save_to_json(metadata, os.path.join(output_path, output_file_name))

def save_to_json(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/transcribe_podcast.py <input_audio_or_youtube_url>")
        sys.exit(1)
    
    input_data = sys.argv[1]
    output_directory = 'output/podcasts'
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    process_input(input_data, output_directory)