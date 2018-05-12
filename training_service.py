from __future__ import print_function
import sys
import base64
import requests
import os
from time import gmtime, strftime

def get_wave(fname):
    with open(fname) as file:
        return base64.b64encode(file.read())

endpoint = "https://snowboy.kitt.ai/api/v1/train/"

token = "b66ed4144412451a0d196da69a5d2251f4d95571"
microphone = "microphone"
out_dir="models"
if(not os.path.exists(out_dir)):
    os.makedirs(out_dir)

def get_model(hotword_name, wave_files, language, age_group, gender):
    print('Training model...')
    wav1, wav2, wav3 = wave_files
    data = {
        "name": hotword_name,
        "language": language,
        "age_group": age_group,
        "gender": gender,
        "microphone": microphone,
        "token": token,
        "voice_samples": [
            {"wave": get_wave(wav1)},
            {"wave": get_wave(wav2)},
            {"wave": get_wave(wav3)}
        ]
    }

    response = requests.post(endpoint, json=data)
    timestamp = strftime("%m-%d-%Y-%H:%M:%S", gmtime())
    out = out_dir + '/' +timestamp + '-' + hotword_name + '.pmdl'
    if(response.ok):
        with open(out, 'w') as file:
            file.write(response.content)
        print("Saved model to {}".format(out))
        return response.ok, out
    else:
        print("Failed")
        print(response.text)
        return response.ok, response.text