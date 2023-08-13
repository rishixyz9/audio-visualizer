from pytube import YouTube
import ffmpeg
import os

def getWav(url):
    stream = YouTube(url).streams.get_audio_only().download()  # Get the URL of the video stream
    os.rename(stream, 'audio.mp4')


    audio, err = (
        ffmpeg
        .input('audio.mp4')
        .output("pipe:", audio_bitrate=4069, format='wav', ar=44100, acodec='pcm_s16le')  # Select WAV output format, and pcm_s16le auidio codec. My add ar=sample_rate
        .run(capture_stdout=True)
    )

    # Write the audio buffer to file for testing
    with open('audio.wav', 'wb') as f:
        f.write(audio)
        os.remove('audio.mp4')