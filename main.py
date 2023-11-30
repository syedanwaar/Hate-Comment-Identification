from api_communications import *

filename = "./sample_audio2.mp3"

audio_url = upload(filename)
print(get_transcript(audio_url))





