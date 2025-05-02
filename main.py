import random
import os
import inspect

import ffmpeg

def randFile(folder):
    path = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))) + "/" + folder
    return path + "/" + random.choice(os.listdir(path))

stream = ffmpeg.input(randFile("video"))
stream = ffmpeg.output(stream, "output.mp4")
ffmpeg.run(stream)