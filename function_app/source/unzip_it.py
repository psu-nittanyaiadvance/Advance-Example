import zipfile
import os
import json

# Define paths
base_path = r"source"
zip_dir = os.path.join(base_path, "Drop Zip Here")
extract_to = os.path.join(base_path, "Main_data")
processed_files_path = os.path.join(zip_dir, "processed_files.json")

# Ensure processed_files.json exists, creating it if not
if not os.path.exists(processed_files_path):
    with open(processed_files_path, 'w') as f:
        json.dump([], f)  # Initialize with an empty list

# Function to load processed files
def load_processed_files():
    with open(processed_files_path, 'r') as f:
        return json.load(f)

# Function to save processed files
def save_processed_file(file_name):
    processed_files = load_processed_files()
    processed_files.append(file_name)
    with open(processed_files_path, 'w') as f:
        json.dump(processed_files, f)

# Function to unzip files
def unzip_file(zip_path, extract_to):
    os.makedirs(extract_to, exist_ok=True)  # Ensure extraction folder exists
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Unzipped {zip_path} to {extract_to}")

# Main logic to process each zip file in the directory
if __name__ == "__main__":
    processed_files = load_processed_files()  # Load list of processed files
    
    # Loop through each zip file in the zip directory
    for zip_file in os.listdir(zip_dir):
        if zip_file.endswith('.zip') and zip_file not in processed_files:
            zip_path = os.path.join(zip_dir, zip_file)
            unzip_file(zip_path, extract_to)
            save_processed_file(zip_file)  # Mark file as processed
        elif zip_file in processed_files:
            print(f"Skipping {zip_file} as it has already been processed.")
