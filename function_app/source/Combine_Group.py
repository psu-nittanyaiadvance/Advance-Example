import os
import re
import shutil

def clean_project_name(filename):
    """
    Cleans the project name by removing date suffixes and extra descriptors like 'Supporting Documents'.
    """
    # Remove any date suffix
    name = re.sub(r"_\d{2}-\d{2}-\d{2}", "", filename)
    # Remove descriptors like 'Supporting Documents'
    name = re.sub(r" Supporting Documents", "", name, flags=re.IGNORECASE)
    return name.strip()

def organize_project_files(output_txt_folder, video_output_folder, project_folder):
    """
    Organizes all files from output_txt and video_output folders into project subfolders in project_folder.
    """
    # Ensure the main project folder exists
    os.makedirs(project_folder, exist_ok=True)

    # Get list of files in both folders
    output_txt_files = os.listdir(output_txt_folder)
    video_output_files = os.listdir(video_output_folder)

    # Process files from output_txt folder
    for filename in output_txt_files:
        project_name = clean_project_name(filename.split("-", 1)[-1].split(".")[0])
        project_subfolder = os.path.join(project_folder, project_name)

        # Ensure the subfolder exists
        os.makedirs(project_subfolder, exist_ok=True)

        # Copy the file to the project folder
        file_path = os.path.join(output_txt_folder, filename)
        shutil.copy(file_path, project_subfolder)

    # Process files from video_output folder
    for filename in video_output_files:
        project_name = clean_project_name(filename.split("-", 1)[-1].split(".")[0])
        project_subfolder = os.path.join(project_folder, project_name)

        # Ensure the subfolder exists
        os.makedirs(project_subfolder, exist_ok=True)

        # Copy the file to the project folder
        file_path = os.path.join(video_output_folder, filename)
        shutil.copy(file_path, project_subfolder)

    print("All files organized into project folders.")

if __name__ == "__main__":
    # Define paths based on the provided folder structure
    output_txt_folder = os.path.join(os.path.dirname(__file__), "output_txt")
    video_output_folder = os.path.join(os.path.dirname(__file__), "video_output")
    project_folder = os.path.join(os.path.dirname(__file__), "Project_folder")

    organize_project_files(output_txt_folder, video_output_folder, project_folder)
