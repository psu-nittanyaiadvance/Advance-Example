import os
import time
import json
import logging
import requests
from azure.storage.blob import BlobServiceClient
import azure.functions as func
from source.Main import save_file, execute_scripts

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR,"source", "Final Results", "Markdown Judge")

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.info(f"Resolved OUTPUT_FOLDER path: {OUTPUT_FOLDER}")


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.function_name(name="prototype-wizard")
@app.queue_trigger(arg_name="msg", queue_name="prototype-wizard-llm-queue", connection="AzureWebJobsStorage")
def prototype_wizard_llm(msg: func.QueueMessage):
    logging.info('Python queue trigger function processed a request.')

    msg_body = json.loads(msg.get_body().decode('utf-8'))

    email = msg_body.get('email')
    team_name = msg_body.get('team_name')
    folder = msg_body.get('folder_name')  
    pdf_name = msg_body.get('file1_name')
    video_name = msg_body.get('file2_name')

    if email:
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage"))
        container_client = blob_service_client.get_container_client("file-uploads")

        # Download the PDF file
        pdf_blob_client = container_client.get_blob_client(f"{folder}/{pdf_name}")
        pdf_content = pdf_blob_client.download_blob().readall()

        # Download the video file
        video_blob_client = container_client.get_blob_client(f"{folder}/{video_name}")
        video_content = video_blob_client.download_blob().readall()

        # Save files using Main.py logic
        save_file(pdf_content, pdf_name, "pdfs")
        save_file(video_content, video_name, "videos")

        # Execute processing pipeline
        logging.info("Executing Main.py processing pipeline...")
        execute_scripts()

        # Wait for output to appear in the output folder
        output_file_path = None
        max_wait_time = 600  # Wait up to 600 seconds (10 minutes)
        poll_interval = 5  # Check every 5 seconds

        logging.info(f"Waiting for output in folder: {OUTPUT_FOLDER} for up to {max_wait_time} seconds...")
        for elapsed_time in range(0, max_wait_time, poll_interval):
            output_files = [
                f for f in os.listdir(OUTPUT_FOLDER) if os.path.isfile(os.path.join(OUTPUT_FOLDER, f))
            ]
            if output_files:
                # Pick the first file (you can adjust logic if needed)
                output_file_path = os.path.join(OUTPUT_FOLDER, output_files[0])
                logging.info(f"Found output file: {output_file_path}")
                break

            # Log progress every minute
            if elapsed_time % 60 == 0:
                logging.info(f"Still waiting for output... {elapsed_time} seconds elapsed.")

            time.sleep(poll_interval)

        if not output_file_path:
            logging.error(f"No output found in folder: {OUTPUT_FOLDER} after {max_wait_time} seconds.")
            return

        # Read the content of the output file to include in the email payload
        with open(output_file_path, 'r', encoding='utf-8') as f:
            processed_output = f.read()

        # API payload
        payload = {
            "email-results": processed_output,
            "email": email,
            "team_name": team_name
        }

        # Call the API endpoint
        api_url = os.getenv("POWER_AUTOMATE_API_URL")
        response = requests.post(api_url, json=payload)

        # Log the response
        logging.info(f"API Response: {response.status_code}")
        if response.status_code != 200:
            logging.error(f"Error sending email: {response.text}")
    else:
        logging.error("Error: Email not found in message body.")
    