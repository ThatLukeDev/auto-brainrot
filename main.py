import ffmpeg
import random

def randFile(path):
    return random.choice(os.listdir(path))

stream = ffmpeg.input(randFile("video"))
stream = ffmpeg.hflip(stream)
stream = ffmpeg.output(stream, 'output.mp4')
ffmpeg.run(stream)