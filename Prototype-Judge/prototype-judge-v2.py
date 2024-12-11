import openai
import os
from dotenv import load_dotenv
import openai
from PyPDF2 import PdfReader
import re


# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

openai.api_type = "azure"
openai.api_base = endpoint 
openai.api_version = "2024-08-01-preview"  # Adjust the version based on your Azure resource setup
openai.api_key = api_key 

def judge_submission(examples, submission):
    prompt = f"""
    Please evaluate the following AI-based prototype idea using the specified criteria and scoring system:

   ### Criteria for evaluation:

    **1. Innovation and Technical Merit (Score 1-10)**

    - Does the prototype demonstrate a novel use of AI, or does it improve upon existing solutions in a significant way?
    - Is the underlying AI model robust, accurate, and efficient?
    - How well has the team addressed potential technical challenges and limitations of their solution?

    **2. Impact and Relevance (Score 1-10)**

    - Does the prototype address a pressing or significant issue within its chosen area (education, environment, humanitarianism, health)?
    - How scalable is the solution, and what potential does it have to create widespread positive change?
    - Is there clear evidence or data supporting the prototype's potential impact?

    **3. User Experience and Accessibility (Score 1-10)**

    - Is the prototype user-friendly, intuitive, and accessible to a diverse range of users, including those with disabilities?
    - How well has the team considered the cultural, socio-economic, and demographic differences of potential users?
    - Are there mechanisms in place to collect user feedback and iterate upon it?

    **4. Ethical Considerations (Score 1-10)**

    - How well does the prototype address potential ethical concerns, including data privacy, fairness, and transparency?
    - Is there a plan in place to handle unintended consequences or misuse of the technology?
    - Has the team demonstrated an understanding of the broader societal implications of their solution?

    **5. Feasibility and Implementation (Score 1-10)**

    - How realistic is the prototype's implementation in real-world scenarios?
    - Is there a clear roadmap for moving from the prototype stage to full deployment?
    - Has the team considered the economic, infrastructural, and regulatory challenges of their solution?

    **Instructions**
    1. Evaluate this prototype submission: {submission}. 
    """

    response = openai.ChatCompletion.create(
        deployment_id="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI judge."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature = 0
    )
    print(prompt)
    return response['choices'][0]['message']['content']

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
    # criteria = """
    #         I would like you to evaluate an AI-based prototype idea using five key criteria: 
    #         1. Impact (10 points)
    #         2. Feasibility (10 points)
    #         3. Implementation & Scaling (10 points)
    #         4. Team Capabilities (10 points)
    #         5. Technical Sophistication (10 points)
    #         6. Use of AI & ML Technologies (5 points)
    #         7. Use of Available Data (5 points)
    #         8. Interface Design Plans/Consumability (5 points)
    #         For each criterion, I need scores from 1 to 10 or 1 to 5 (The higher number, the better, 65 points in total). 
    #         Here is the submission:
    #         """
    # prompt = criteria + submission
    completion = comments
    json = {"prompt": submission, "completion": completion}
    return json


if __name__=="__main__":

    directory = 'Prototype-Judge/challenge-data/2023-top10'
    test_directory = 'Prototype-Judge/challenge-data/2023-top10-test'

    pdf_paths_list = []
    test_pdf_paths_list = []

    pdf_files_list = []
    test_pdf_files_list = []

    judge_comments = None
    json_list = []

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):  
            joined_path = os.path.join(directory, filename)
            pdf_paths_list.append(os.path.normpath(joined_path))

    for filename in os.listdir(test_directory):
        if filename.endswith('.pdf'):  
            test_joined_path = os.path.join(test_directory, filename)
            test_pdf_paths_list.append(os.path.normpath(test_joined_path))

    for pdf_file_path in pdf_paths_list:
        pdf_files_list.append(extract_text(pdf_file_path))

    for test_pdf_file_path in test_pdf_paths_list:
        test_pdf_files_list.append(extract_text(test_pdf_file_path))

    with open('Prototype-Judge/challenge-data/2023-top10/2023-judge-comments.txt', 'r') as filename:
        judge_comments = filename.read()

    judge_comments_list = judge_comments.split('\n\n')

    for pdf, judge_comment in zip(pdf_files_list, judge_comments_list):
        json_object = judge_comment
        #create_json(pdf, judge_comment)
        json_list.append(json_object)

    result_list = []
    # for json_object, test_pdf in zip(json_list, test_pdf_files_list):
    #     result_list.append(judge_submission(json_object, test_pdf))

    # manually change the input
    result_list.append(judge_submission(json_list[0], test_pdf_files_list[0]))

    with open("Prototype-Judge\judge_output_Therapeutrack.txt", "w") as file:
        for result in result_list:
            file.write(result + "\n")

    print("Output saved to judge_output.txt")