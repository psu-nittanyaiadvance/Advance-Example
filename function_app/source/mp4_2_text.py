import os
import datetime
import subprocess
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event


# Load environment variables from .env file
load_dotenv()

# Retrieve the Azure Speech API key and region from environment variables
speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_REGION")

# Dictionary to track processed video files
processed_files = {}

import os
import subprocess

def extract_audio_from_video(video_path):
    """
    Extracts audio from the video file using ffmpeg.
    """
    # Define the path to the ffmpeg binary
    ffmpeg_path = os.path.join(os.getcwd(), "bin", "ffmpeg")
    
    # Set the path for the extracted audio file
    audio_path = f"{os.path.splitext(video_path)[0]}.wav"
    
    # Check if the audio file already exists to avoid re-extraction
    if not os.path.exists(audio_path):
        # Extract audio using ffmpeg
        print(f"Extracting audio from {video_path} to {audio_path}")
        try:
            subprocess.run(
                [ffmpeg_path, "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"], 
                #["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,  # Capture ffmpeg output for error handling
                text=True  # Ensure output is captured as a string
            )
        except subprocess.CalledProcessError as e:
            if "Stream map 'a' matches no streams" in e.stderr:
                # No audio found in the video
                print(f"No sound found in {video_path}, continuing with the other processes.")
                return None  # Indicate that no audio was extracted
            else:
                # Other ffmpeg-related errors
                print(f"Error occurred during audio extraction: {e.stderr}")
                raise
    return audio_path


def transcribe_audio_with_azure(audio_path):
    """
    Transcribes audio to text using Azure's Speech-to-Text service.
    Supports longer audio files by leveraging continuous recognition.
    """
    if not speech_key or not service_region:
        raise ValueError("Azure Speech API key and region must be set in the .env file.")
    
    print(f"Transcribing audio from {audio_path}")

    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    audio_input = AudioConfig(filename=audio_path)
    speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    # Storage for recognized text
    transcript = []
    done = Event()

    def handle_recognized(evt):
        # Append recognized speech to the transcript
        transcript.append(evt.result.text)
        print(f"Recognized: {evt.result.text}")

    def handle_completed(evt):
        print(f"Transcription completed for {audio_path}")
        done.set()  # Signal that the transcription is done

    def handle_canceled(evt):
        print(f"Transcription canceled. Reason: {evt.reason}")
        done.set()  # Signal that the transcription is done

    # Hook events
    speech_recognizer.recognized.connect(handle_recognized)
    speech_recognizer.session_stopped.connect(handle_completed)
    speech_recognizer.canceled.connect(handle_canceled)

    # Start continuous recognition
    speech_recognizer.start_continuous_recognition()
    print("Waiting for transcription to complete...")
    done.wait()  # Wait until transcription is complete

    # Stop recognition
    speech_recognizer.stop_continuous_recognition()

    return " ".join(transcript)  # Return full transcript

def transcribe_video(video_path):
    """
    Extracts audio from a video file and transcribes it.
    """
    audio_path = extract_audio_from_video(video_path)
    
    if audio_path is None:
        # No audio was extracted, skip transcription
        print(f"Skipping transcription for {video_path} due to lack of audio.")
        return None

    transcript = transcribe_audio_with_azure(audio_path)
    os.remove(audio_path)  # Clean up the extracted audio
    return transcript


def save_transcript_to_file(transcript, output_file):
    """
    Saves the transcript to a specified file.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(transcript)
    print(f"Transcript saved to {output_file}")

def process_video_file(video_path, output_folder):
    """
    Process an individual video file: transcribe and save transcript.
    """
    filename = os.path.basename(video_path)
    file_date = datetime.datetime.now().strftime("%d-%m-%y")
    txt_filename = f"{os.path.splitext(filename)[0]}_video_{file_date}.txt"
    output_txt_path = os.path.join(output_folder, txt_filename)

    # Check if the video has already been processed
    if filename not in processed_files:
        processed_files[filename] = 1  # Initialize with a count of 1
    else:
        print(f"{filename} has already been processed {processed_files[filename]} time(s). Skipping.")
        return

    # Process the video and update the processed files dictionary
    transcript = transcribe_video(video_path)
    
    if transcript:
        save_transcript_to_file(transcript, output_txt_path)
        processed_files[filename] += 1  # Increment count each time the file is processed

def process_videos_in_folder(folder_path, output_folder="video_output"):
    """
    Processes all video files in a folder concurrently, transcribing their content to individual .txt files.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder at {folder_path}. Please place videos here and re-run the script.")
        return

    os.makedirs(output_folder, exist_ok=True)

    # Load or initialize the dictionary of processed files
    load_processed_files(output_folder)

    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))]

    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in video_files:
            video_path = os.path.join(folder_path, filename)
            futures.append(executor.submit(process_video_file, video_path, output_folder))

        for future in as_completed(futures):
            future.result()  # This will raise exceptions if the task encountered an error

    # Save the updated processed files dictionary
    save_processed_files(output_folder)

def load_processed_files(output_folder):
    """
    Loads the dictionary of processed files from a file in the output folder.
    """
    global processed_files
    processed_file_path = os.path.join(output_folder, "processed_files.txt")

    if os.path.exists(processed_file_path):
        with open(processed_file_path, 'r') as f:
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespace
                if line:  # Skip empty lines
                    try:
                        name, count = line.split(',')
                        processed_files[name] = int(count)
                    except ValueError:
                        print(f"Skipping malformed line: {line}")  # Log any malformed lines

def save_processed_files(output_folder):
    """
    Saves the dictionary of processed files to a file in the output folder.
    """
    processed_file_path = os.path.join(output_folder, "processed_files.txt")
    with open(processed_file_path, 'w') as f:
        for name, count in processed_files.items():
            f.write(f"{name},{count}\n")


folder_path = os.path.join(os.path.dirname(__file__), "videos")
output_folder = os.path.join(os.path.dirname(__file__), "video_output")
process_videos_in_folder(folder_path, output_folder)
