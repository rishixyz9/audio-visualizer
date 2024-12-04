from pytube import YouTube
import youtube_dl
import yt_dlp
import ffmpeg
import os


def getWav(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "audio.%(ext)s",  # Specify output filename template
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # stream = (
    #     YouTube(url).streams.get_audio_only().download()
    # )  # Get the URL of the video stream
    # os.rename(stream, "audio.mp4")

    audio, err = (
        ffmpeg.input("audio.mp3")
        .output(
            "pipe:", audio_bitrate=4069, format="wav", ar=44100, acodec="pcm_s16le"
        )  # Select WAV output format, and pcm_s16le auidio codec. My add ar=sample_rate
        .run(capture_stdout=True)
    )

    # Write the audio buffer to file for testing
    with open("audio.wav", "wb") as f:
        f.write(audio)
        os.remove("audio.mp3")
