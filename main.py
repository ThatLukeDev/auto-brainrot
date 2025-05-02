import random
import os
import inspect
import datetime

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
    audio = randClip("audio", duration)
    stream = ffmpeg.output(audio, video, "output.mp4")
    ffmpeg.run(stream, overwrite_output=True)

randBackground(1)