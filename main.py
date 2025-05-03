MODEL = "qwen3"
PROMPT = """
Generate a script for a brainrot youtube video.
Make sure to use the exact form:

<title>VIDEO TITLE HERE</title>
<tags>CSV TAGS HERE</tags>
<speech>CONTENT HERE</speech>

You must only include speech read to the user in the speech tag. The video will show a random background footage and captions. Here is an example:

<title>Skibidi Ohio Rizz</title>
<tags>#brainrot,#skibidi</tags>
<speech>My great grandfather once said, you bite not hand not that then what feed. Great word once spoke.</speech>

Here the humour comes from not understanding the speech. In each instance, formulate a plan that makes it unexpected.
You should not only rely on the same type of humour, as it becomes repetivie. Formulate your own idea for humour.
"""

import random
import os
import inspect
import datetime
import math
import requests
import uuid
import time

import ffmpeg
import ollama

def randFile(folder):
    path = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))) + "/" + folder
    return path + "/" + random.choice(os.listdir(path))

def randClip(folder, duration):
    path = randFile(folder)
    videoLen = eval(ffmpeg.probe(path)["format"]["duration"])
    start = random.randint(0, int(videoLen - duration))
    stream = ffmpeg.input(path, ss=str(datetime.timedelta(seconds=start)), to=str(datetime.timedelta(seconds=start+duration)))
    return stream

def randBackground(duration):
    video = randClip("video", duration)
    video = video.filter("scale", 1920, 1080).crop(420, 0, 960, 1080).filter("scale", 1080, 1920)

    audio = randClip("audio", duration)
    audio = audio.filter("loudnorm").filter("volume", 0.05 + 20 * math.exp(-1000 * random.random() ** 2))

    stream = ffmpeg.output(audio, video, "background.mp4")
    ffmpeg.run(stream, overwrite_output=True)

def genScript():
    response = ollama.chat(model=MODEL, messages=[
    {
        "role": "user",
        "content": PROMPT,
    },
    ])
    text = response['message']['content'].split("</think>\n\n")[1]
    return text

def speak(text):
    response = requests.post("https://api.fakeyou.com/tts/inference", json = {
        "inference_text": text,
        "tts_model_token": "weight_3k28fws0v6r1ke3p0w0vw48gm",
        "uuid_idempotency_token": str(uuid.uuid4())
    }).json()

    if response["success"] == False:
        return

    token = response["inference_job_token"]

    for i in range(1, 30):
        time.sleep(i)
        response = requests.get("https://api.fakeyou.com/v1/model_inference/job_status/" + token).json()
        if response["state"]["status"]["progress_percentage"] == 100:
            break

    response = requests.get(response["state"]["maybe_result"]["media_links"]["cdn_url"]).content

    with open("audio.wav", "wb") as file:
        file.write(response)

def brainrot(text):
    # speak(text)
    duration = ffmpeg.probe("audio.wav")["streams"][0]["duration"]

    randBackground(math.floor(float(duration)) + 2)

    stream = ffmpeg.input("background.mp4")
    video = stream.video
    audio = stream.audio
    speech = ffmpeg.input("audio.wav")
    audio = ffmpeg.filter([audio, speech], "amix")

    stream = ffmpeg.output(video, audio, "output.mp4", **{'c:v': 'copy', 'c:a': 'aac'})
    ffmpeg.run(stream, overwrite_output=True)

brainrot("Whats going on guys!")