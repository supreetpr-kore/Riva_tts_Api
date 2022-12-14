
from flask import Flask, jsonify, request,  Response, send_file, make_response
import numpy as np
# import IPython.display as ipd
import riva.client
from scipy.io.wavfile import write



auth = riva.client.Auth(uri='localhost:50051')

riva_tts = riva.client.SpeechSynthesisService(auth)
 
app = Flask(__name__)

@app.route('/tts/healthcheck')
def healthcheck():
    response = {}
    response["server_status"] = "Server is up and running"
    resp = make_response(response, 200)
    return resp

# GET requests will be blocked
@app.route('/tts', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['language']
    format_data = request_data['format']
    encoding = request_data['encoding']
    sampleRateHz = request_data['sampleRateHz']
    voice = request_data['voice']
    text = request_data['text']
    print(sampleRateHz)
    print(format_data)

    audio_samples = get_audio_strem(text, sample_rate_hz = sampleRateHz , language_code = language ,encoding = encoding , voice_name = voice)
    print(type(audio_samples))
    return Response(audio_samples.audio, mimetype="audio/x-wav;codec=pcm;rate="+str(sampleRateHz))

def get_audio_strem(text, sample_rate_hz = 44100,language_code = "en-US",encoding =  "LINEAR16" , voice_name = "English-US-Female-1"):
    #sample_rate_hz = 44100
    if encoding == "LINEAR16":
        encoding = riva.client.AudioEncoding.LINEAR_PCM
    resp = riva_tts.synthesize(
        text =text,
        language_code = "en-US",
        encoding = encoding,    # Currently only LINEAR_PCM is supported
        sample_rate_hz = sample_rate_hz,                    # Generate 44.1KHz audio
        voice_name = voice_name                  # The name of the voice to generate
    
    )
    print(sample_rate_hz)
    audio_samples = np.frombuffer(resp.audio, dtype=np.int16)
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
