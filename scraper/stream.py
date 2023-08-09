from pytube import YouTube
import ffmpeg




def getWav(url):
    stream_url = YouTube(url).streams.all()[0].url  # Get the URL of the video stream

    audio, err = (
        ffmpeg
        .input(stream_url)
        .output("pipe:", audio_bitrate=4069, format='wav', ar=44100, acodec='pcm_s16le')  # Select WAV output format, and pcm_s16le auidio codec. My add ar=sample_rate
        .run(capture_stdout=True)
    )

    # Write the audio buffer to file for testing
    with open('audio.wav', 'wb') as f:
        f.write(audio)