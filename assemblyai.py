import io
import requests
import globals
import time

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

# uploads a file to assemblyai
# returns the upload url on success
# returns None otherwise
def uploadFile(data):
    endpoint = 'https://api.assemblyai.com/v2/upload'
    headers = { "authorization": globals.ASSEMBLYAI_API_KEY }
    response = requests.post(endpoint, headers=headers, data=data).json()
    # print(response)
    return None if 'error' in response else response['upload_url']

# get the status of a pending transcript by id
# returns a response object on success
# returns None otherwise
def getPendingTranscript(id):
    endpoint = 'https://api.assemblyai.com/v2/transcript/' + id
    # print(endpoint)
    headers = { 
        "authorization": globals.ASSEMBLYAI_API_KEY,
        "content-type": "application/json",
    }
    response = requests.get(endpoint, headers=headers).json()
    # print(response)
    return None if 'error' in response else response

# start the transcript
# returns a response object on success
# returns None otherwise
def startTranscript(audioURL, lang):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": audioURL,
        "language_code": lang,
    }
    headers = {
        "authorization": globals.ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers).json()
    # print(response)
    return None if 'error' in response else response

def getTranscript(audioFilePath, lang = 'es'):
    print("API key = " + globals.ASSEMBLYAI_API_KEY)
    # read file
    audio = read_file(audioFilePath)

    # upload file
    audioUrl = uploadFile(audio)
    if audioUrl is None:
        print('error occurred when uploading file')
        return ''

    # make transcript request
    response = startTranscript(audioUrl, lang)
    if response is None:
        print('error occurred when starting transcript')
        return ''
    id = response['id']
    while True:
        print('waiting ...')
        time.sleep(5)
        pending = getPendingTranscript(id)
        if pending is None:
            continue
        match pending['status']:
            case 'completed':
                print('done!')
                break
            case 'processing':
                print('processing ..')
            case 'queued':
                print('queued ..')
            case 'error':
                print('error occurred when pinging server')
                return ''
    return pending['text']

