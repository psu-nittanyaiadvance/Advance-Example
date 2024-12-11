import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Base path for all operations - corrected to current script's directory
base_path = os.path.dirname(__file__)

# Define folder paths relative to the current base path
folders = [
    #"Final Results",
    "output_txt",
    "pdfs",
    "Project_folder",
    "videos",
    "video_output"
]

# Create folders if they don't already exist
for folder in folders:
    folder_path = os.path.join(base_path, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        #print(f"Created folder: {folder_path}")
    #else:
        #print(f"Folder already exists: {folder_path}")

# Function to save files into specific folders
def save_file(content, filename, folder):
    folder_path = os.path.join(base_path, folder)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "wb") as file:
        file.write(content)
    #print(f"Saved {filename} to {folder}")

# Define the list of scripts to run in order
scripts = [
    #"Sort.py",
    "Text_extractor.py",  # to run concurrently
    "mp4_2_text.py",      # to run concurrently
    "Combine_Group.py",
    "Judge.py"
]

# Function to run a Python script
def run_script(script_name):
    script_path = os.path.join(base_path, script_name)
    python_executable = "python"
    print(f"Running {script_path} with {python_executable}...")
    result = subprocess.run([python_executable, script_path], capture_output=True, text=True)
    print(f"Finished {script_name} with output:\n{result.stdout}")
    if result.stderr:
        print(f"Error in {script_name}:\n{result.stderr}")


# Execute scripts sequentially
def execute_scripts():
    with tqdm(total=len(scripts), desc="Running Scripts", unit="script") as pbar:
        for script in scripts:
            run_script(script)
            pbar.update(1)

# Main entry point for the script
if __name__ == "__main__":
    print("Starting script execution...")
    execute_scripts()
    print("All scripts executed successfully!")
