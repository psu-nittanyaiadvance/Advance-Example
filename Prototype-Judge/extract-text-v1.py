from PyPDF2 import PdfReader
import re

def extract_text(filename):
    reader = PdfReader(filename)
    number_of_pages = len(reader.pages)

    with open("Prototype-Judge/lionfoodtracker.txt", "w", encoding="utf-8") as output_file:
        for page in reader.pages:
            text = page.extract_text()
            text = re.sub(r'(?<=\S) (?=\S)', '', text) # remove spaces between letters
            text = re.sub(r'\s+', ' ', text) # remove extra spaces between words
            output_file.write(text)

    with open("Prototype-Judge/lionfoodtracker.txt", "r", encoding="utf-8") as input_file:
        text = input_file.read()

        # List of section headers
        section_list = ["Overview", "Abstract", "Use Case", "Technology", "Data Sources", "Security/Privacy", "User Interface", "Development Timeline", "Team Capabilities", "References"]

        sections = {}

        # Create a single pattern that matches any section header from the list
        pattern = '|'.join([re.escape(section) for section in section_list])

        # Find the positions of all the headers
        matches = list(re.finditer(pattern, text))

        # Loop through the matches and extract text between headers
        for i in range(len(matches)):
            # Get the start position of the current match and the next match
            start_pos = matches[i].end() # right after the section name
            end_pos = matches[i+1].start() if i + 1 < len(matches) else len(text)
            
            # Extract the header and content
            section_header = matches[i].group()
            section_content = text[start_pos:end_pos].strip()  # Get content between headers
            
            # Store in the dictionary
            sections[section_header] = section_content

        # Output the result
        for section, content in sections.items():
            print(f"Section: {section}")
            print(f"Content: {content}\n")

def main():
    filename = "Prototype-Judge/LionFoodTracker.pdf"
    extract_text(filename)

main()