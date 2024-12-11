import os
import shutil
import json

# Define paths
MAIN_DATA_FOLDER = "source/Main_data"
PDFS_FOLDER = "source/pdfs"
VIDEOS_FOLDER = "source/videos"
BACKBRAIN_FOLDER = "source/Backbrain"
TRACKING_FILE = os.path.join(BACKBRAIN_FOLDER, "file_tracking.json")

# Ensure destination folders exist
os.makedirs(PDFS_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)
os.makedirs(BACKBRAIN_FOLDER, exist_ok=True)  # Ensure Backbrain folder exists

# Load or initialize tracking dictionary
if os.path.exists(TRACKING_FILE):
    with open(TRACKING_FILE, 'r') as f:
        file_tracking = json.load(f)
else:
    file_tracking = {}

# Function to sort files
def sort_files():
    # List all files in the main data folder
    for filename in os.listdir(MAIN_DATA_FOLDER):
        file_path = os.path.join(MAIN_DATA_FOLDER, filename)
        
        # Skip if it's a directory
        if os.path.isdir(file_path):
            continue

        # Check if the file has already been processed
        if file_tracking.get(filename) == "seen":
            print(f"{filename} has already been processed. Skipping.")
            continue

        # Check file extension and copy accordingly
        if filename.lower().endswith('.pdf'):
            shutil.copy(file_path, os.path.join(PDFS_FOLDER, filename))
            #print(f"Copied PDF: {filename}")
        else:
            shutil.copy(file_path, os.path.join(VIDEOS_FOLDER, filename))
            #print(f"Copied Video/Other: {filename}")

        # Mark the file as seen in the tracking dictionary
        file_tracking[filename] = "seen"

    # Save the updated tracking dictionary to file
    with open(TRACKING_FILE, 'w') as f:
        json.dump(file_tracking, f)

if __name__ == "__main__":
    sort_files()
