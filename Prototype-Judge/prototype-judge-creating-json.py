from PyPDF2 import PdfReader
import re
import os
import json as js

def extract_text(filename):
    try:
        reader = PdfReader(filename)
        full_text = ""

        for page in reader.pages:
            text = page.extract_text() or ""
            text = re.sub(r'(?<=\S) (?=\S)', '', text)  # Remove spaces between letters
            text = re.sub(r'\s+', ' ', text)  # Remove extra spaces between words
            
            # Normalize quotes if needed
            text = text.replace('“', '"').replace('”', '"')  # Normalize double quotes
            text = text.replace("‘", "'").replace("’", "'")  # Normalize single quotes
            text = text.replace('"', '\\"').replace("'", "\\'")
            text = text.replace('\n', '\\n') 

            full_text += text + " "

        return full_text.strip()  # Trim any trailing spaces

    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def create_json(submission, comments):
    criteria = """
            I would like you to evaluate an AI-based prototype idea using five key criteria: 
            1. Impact (10 points)
            2. Feasibility (10 points)
            3. Implementation & Scaling (10 points)
            4. Team Capabilities (10 points)
            5. Technical Sophistication (10 points)
            6. Use of AI & ML Technologies (5 points)
            7. Use of Available Data (5 points)
            8. Interface Design Plans/Consumability (5 points)
            For each criterion, I need scores from 1 to 10 or 1 to 5 (The higher number, the better, 65 points in total). 
            Here is the submission:
            """
    # prompt = criteria + submission
    prompt = submission
    completion = comments
    json = {"submission": prompt, "comments": completion}
    return json

def chunk_text(text, max_length=512):
    # Split the text into words/tokens
    tokens = text.split()  
    chunks = []
    current_chunk = []

    for token in tokens:
        # Add the token to the current chunk
        current_chunk.append(token)

        # Check if the current chunk exceeds the max length
        if len(current_chunk) >= max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    # Add any remaining tokens as a final chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def main():
    directory = 'challenge-data/prototype-judge-2024/llm-example'
    pdf_paths_list = []
    pdf_files_list = []
    judge_comments = None
    json_list = []

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):  
            joined_path = os.path.join(directory, filename)
            pdf_paths_list.append(os.path.normpath(joined_path))

    for pdf_file_path in pdf_paths_list:
        pdf_files_list.append(extract_text(pdf_file_path))

    with open('challenge-data/prototype-judge-2024/judge-comments-example-2024.txt', 'r') as filename:
        judge_comments = filename.read()

    judge_comments_list = judge_comments.split('\n\n')

    for pdf, judge_comment in zip(pdf_files_list, judge_comments_list):
        json_object = create_json(pdf, judge_comment)
        json_list.append(json_object)

    # Open the JSONL file for writing
    with open('challenge-data/prototype-judge-2024/llm-example-2024.jsonl', 'w') as jsonl:
        for json_object in json_list:
            try:
                # Convert the dictionary to a JSON string
                json_string = js.dumps(json_object)

                # Validate the JSON string by loading it back
                js.loads(json_string)  # This will raise an error if json_string is not valid

                # If valid, write it to the JSONL file
                jsonl.write(json_string + '\n')  # Ensure each object ends with a newline

            except Exception as e:
                print(f"JSON Error: {e}")  # Print error if validation fails

main()
