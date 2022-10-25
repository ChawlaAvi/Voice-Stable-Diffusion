import os
import streamlit as st
import streamlit.components.v1 as components
import requests
import numpy as np 
from io import BytesIO
import replicate
from time import sleep

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
st_audiorec = components.declare_component("st_audiorec", path=build_dir)


assembly_auth_key = "535b2431381742b297a92085de5c951c"

headers = {
    'authorization': assembly_auth_key, 
    'content-type': 'application/json',
}

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcription_endpoint = "https://api.assemblyai.com/v2/transcript"


def record_audio(file_path):

    val = st_audiorec()

    st.write('Audio data received in the Python backend will appear below this message ...')

    if isinstance(val, dict):  # retrieve audio data
        with st.spinner('retrieving audio-recording...'):

            ind, val = zip(*val['arr'].items())
            ind = np.array(ind, dtype=int)  # convert to np array
            val = np.array(val)             # convert to np array
            sorted_ints = val[ind]
            stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            wav_bytes = stream.read()

        st.audio(wav_bytes, format='audio/wav')

        with open(file_path, "wb") as f:
            f.write(wav_bytes)

def upload_to_assemblyai(file_path):

    def read_audio(file_path):

        with open(file_path, 'rb') as f:
            while True:
                data = f.read(5_242_880)
                if not data:
                    break
                yield data

    upload_response =  requests.post(upload_endpoint, 
                                     headers=headers, 
                                     data=read_audio(file_path))

    return upload_response.json().get('upload_url')

def transcribe(upload_url): 

    json = {"audio_url": upload_url}
    
    response = requests.post(transcription_endpoint, json=json, headers=headers)
    transcription_id = response.json()['id']

    return transcription_id

def get_transcription_result(transcription_id): 

    current_status = "queued"

    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"

    while current_status not in ("completed", "error"):
        
        response = requests.get(endpoint, headers=headers)
        current_status = response.json()['status']
        
        if current_status in ("completed", "error"):
            return response.json()['text']
        else:
            sleep(10)

def call_stable_diffusion(prompt):

    model = replicate.models.get("stability-ai/stable-diffusion")
    output_url = model.predict(prompt=prompt)[0]
    
    with open("result_image.jpg", "wb") as f:
        image = requests.get(output_url).content
        f.write(image)

def main():

    st.title("Voice-assited Image Generation with Stable Diffusion")
    file_path = "input.wav"

    record_audio(file_path)

    upload_url = upload_to_assemblyai(file_path)
    st.write('Prompt uploaded to AssemblyAI')

    transcription_id = transcribe(upload_url)
    st.write('Prompt Sent for Transciption to AssemblyAI')

    prompt = get_transcription_result(transcription_id)

    st.write('Prompt Transcribed...Sending to Stable Diffusion')
    st.info(prompt)

    image = call_stable_diffusion(prompt)

    st.write('Response Received from Stable Diffusion')
    st.image("result_image.jpg")

if __name__ == "__main__":
    main()

