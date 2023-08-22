from typing import Union
from fastapi import FastAPI
from urllib.parse import unquote 
import sys

sys.path.append('../')

from scraper.stream import getWav
from recorder.recorder import Recorder

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/getwav/{url}")
def read_item(url: str):
    url = unquote(unquote(url))
    getWav(url)
    return {"url": url}

@app.get("/openstream")
def open_stream(url: str):
    aud_in = Recorder('audio.wav')
    data = aud_in.play()
    return (8)
