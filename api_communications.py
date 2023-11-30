import requests
from api_secrets import API_KEY
import time

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcribe_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization': API_KEY}


# Upload

def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    response = requests.post(upload_endpoint,
                            headers=headers,
                            data=read_file(filename))

    audio_url = response.json()['upload_url']
    return audio_url

# Trasncribe
def transcribe(audio_url):
    json = { "audio_url": audio_url }
    response = requests.post(transcribe_endpoint, json=json, headers=headers)
    job_id = response.json()['id']
    return job_id

# Poll

def poll(transcript_id):
    polling_endpoint = f"{transcribe_endpoint}/{transcript_id}"
    polling_response = requests.get(polling_endpoint,headers=headers)
    return polling_response.json()

def get_transcript_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status']=='completed':
            return data, None
        elif data['status']=='error':
            return data, data['error']
        time.sleep(30)

# Get transcript

def get_transcript(audio_url):
    data, error = get_transcript_result_url(audio_url)
    return data['text']
