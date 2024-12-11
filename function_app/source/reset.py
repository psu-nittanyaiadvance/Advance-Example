import os
import shutil

# Base path for the current directory (since we're inside "source")
base_path = os.path.join(os.getcwd(), "source")  # Current working directory

# List of folders to delete
folders_to_delete = [
    "Backbrain",
    "Final Results",
    "Main_data",
    "output_txt",
    #"pdfs",
    "Project_folder",
    #"videos",
    "video_output"
]

# File to delete
file_to_delete = "processed_files.json"

# Function to delete folders
def delete_folder(folder_name):
    folder_path = os.path.join(base_path, folder_name)
    # Check if the folder exists
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)  # Delete the folder and its contents
            print(f"Deleted folder: {folder_path}")
        except Exception as e:
            print(f"Error deleting {folder_path}: {e}")
    else:
        print(f"Folder does not exist: {folder_path}")

# Function to delete a file
def delete_file(file_name):
    file_path = os.path.join(base_path, file_name)
    # Check if the file exists
    if os.path.exists(file_path):
        try:
            os.remove(file_path)  # Delete the file
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    else:
        print(f"File does not exist: {file_path}")

# Delete each specified folder
for folder in folders_to_delete:
    delete_folder(folder)

# Delete the specified file
delete_file(file_to_delete)

print("\nSpecified folders and file have been deleted.")
