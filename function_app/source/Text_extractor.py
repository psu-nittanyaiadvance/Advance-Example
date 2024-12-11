import fitz  # PyMuPDF
import os
import datetime

processed_files = {}  # Dictionary to track processed PDFs and their process count

def extract_text_from_pdf(pdf_path, output_txt_path, max_pages=50):
    """
    Extracts text from a PDF file and writes it to a .txt file.
    If the PDF is large, it splits the extraction into chunks of pages.
    """
    #print(f"Starting text extraction for: {pdf_path}")
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        print(f"{pdf_path} has {total_pages} pages.")
        chunk = 1

        with open(output_txt_path, 'w', encoding='utf-8') as output_file:
            # Process in chunks
            for start_page in range(0, total_pages, max_pages):
                text = ""
                end_page = min(start_page + max_pages, total_pages)

                for page_num in range(start_page, end_page):
                    page = doc[page_num]
                    text += page.get_text("text")

                # Write extracted text to file, marking each chunk
                output_file.write(f"--- Start of Chunk {chunk} (Pages {start_page+1} to {end_page}) ---\n")
                output_file.write(text)
                output_file.write(f"\n--- End of Chunk {chunk} ---\n\n")

                #print(f"Extracted chunk {chunk} (Pages {start_page+1} to {end_page}) for {pdf_path}.")
                chunk += 1

        #print(f"Text extraction completed successfully for: {pdf_path}. Output: {output_txt_path}")

    except Exception as e:
        print(f"An error occurred while processing {pdf_path}: {e}")


def process_folder(folder_path, output_folder):
    """
    Processes all PDFs in a folder, extracting their content to individual .txt files.
    Creates folder if not found.
    """
    #print(f"Checking folder: {folder_path}")
    # Ensure input folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        #print(f"Created folder at {folder_path}. Please place PDFs here and re-run the script.")
        return

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load or initialize the dictionary of processed files
    load_processed_files(output_folder)

    print(f"Processing PDFs in folder: {folder_path}")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            file_date = datetime.datetime.now().strftime("%d-%m-%y")

            # Initialize file in processed_files if not already present
            if filename not in processed_files:
                processed_files[filename] = 1  # First time processing
            else:
                #print(f"{filename} has already been processed {processed_files[filename]} time(s). Skipping.")
                continue

            # Define the output .txt file path with timestamp
            txt_filename = f"{os.path.splitext(filename)[0]}_text_{file_date}.txt"
            output_txt_path = os.path.join(output_folder, txt_filename)

            # Process the PDF and update the processed files dictionary
            #print(f"Processing {filename}...")
            extract_text_from_pdf(file_path, output_txt_path)
            processed_files[filename] += 1  # Increment count each time the file is processed

    # Save the updated processed files dictionary
    save_processed_files(output_folder)
    print("Processing complete for all PDFs in the folder.")


def load_processed_files(output_folder):
    """
    Loads the dictionary of processed files from a file in the output folder.
    """
    global processed_files
    processed_file_path = os.path.join(output_folder, "processed_files.txt")

    if os.path.exists(processed_file_path):
        #print(f"Loading processed files from: {processed_file_path}")
        with open(processed_file_path, 'r') as f:
            for line in f:
                name, count = line.strip().split(',')
                processed_files[name] = int(count)
        #print("Processed files loaded successfully.")
    else:
        print(f"No processed files record found at: {processed_file_path}. Starting fresh.")


def save_processed_files(output_folder):
    """
    Saves the dictionary of processed files to a file in the output folder.
    """
    processed_file_path = os.path.join(output_folder, "processed_files.txt")
    #print(f"Saving processed files to: {processed_file_path}")
    with open(processed_file_path, 'w') as f:
        for name, count in processed_files.items():
            f.write(f"{name},{count}\n")
    #print("Processed files saved successfully.")

# Example usage
folder_path = os.path.join(os.path.dirname(__file__), "pdfs")
output_folder = os.path.join(os.path.dirname(__file__), "output_txt")
process_folder(folder_path, output_folder)
