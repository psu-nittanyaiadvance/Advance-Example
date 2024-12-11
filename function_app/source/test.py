import requests
import time

# Replace these variables with your own information
SUBSCRIPTION_KEY = 'YOUR_SUBSCRIPTION_KEY'
LOCATION = 'YOUR_LOCATION'  # e.g., 'trial' or 'westus2'
ACCOUNT_ID = 'YOUR_ACCOUNT_ID'
VIDEO_FILE_PATH = 'path/to/your/video.mp4'
VIDEO_NAME = 'My Uploaded Video'

def get_access_token():
    url = f'https://api.videoindexer.ai/Auth/{LOCATION}/Accounts/{ACCOUNT_ID}/AccessToken'
    params = {
        'allowEdit': 'true'
    }
    headers = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.text.strip('"')

def upload_video(access_token):
    url = f'https://api.videoindexer.ai/{LOCATION}/Accounts/{ACCOUNT_ID}/Videos'
    params = {
        'accessToken': access_token,
        'name': VIDEO_NAME,
        'videoUrl': '',  # Leave empty when uploading from local file
    }
    files = {
        'file': open(VIDEO_FILE_PATH, 'rb')
    }
    response = requests.post(url, params=params, files=files)
    response.raise_for_status()
    return response.json()['id']

def check_processing_state(access_token, video_id):
    url = f'https://api.videoindexer.ai/{LOCATION}/Accounts/{ACCOUNT_ID}/Videos/{video_id}/Index'
    params = {
        'accessToken': access_token
    }
    while True:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        state = data.get('state')
        print(f'Video processing state: {state}')
        if state == 'Processed':
            break
        elif state == 'Failed':
            raise Exception('Video processing failed.')
        time.sleep(30)  # Wait for 30 seconds before checking again

def get_transcript(access_token, video_id):
    url = f'https://api.videoindexer.ai/{LOCATION}/Accounts/{ACCOUNT_ID}/Videos/{video_id}/Index'
    params = {
        'accessToken': access_token
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract the transcription text
    transcripts = data['videos'][0]['insights']['transcript']
    full_transcript = ' '.join([t['text'] for t in transcripts])
    return full_transcript

def main():
    print('Getting access token...')
    access_token = get_access_token()
    print('Uploading video...')
    video_id = upload_video(access_token)
    print(f'Video uploaded. Video ID: {video_id}')
    print('Checking video processing state...')
    check_processing_state(access_token, video_id)
    print('Retrieving transcription...')
    transcript = get_transcript(access_token, video_id)
    print('Transcription:')
    print(transcript)

if __name__ == '__main__':
    main()
