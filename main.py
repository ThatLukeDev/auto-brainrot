import random
import os
import inspect
import datetime
import math

import ffmpeg
import ffmpeg.video

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

    stream = ffmpeg.output(audio, video, "output.mp4")
    ffmpeg.run(stream, overwrite_output=True)

randBackground(10)