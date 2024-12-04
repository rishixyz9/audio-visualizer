from fastapi import FastAPI, WebSocket
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

# @app.get("/openstream")
# def open_stream():
#     aud_in = Recorder('audio.wav')
#     data = aud_in.play()
#     return (8)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    aud_in = Recorder('audio.wav')
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        data = None
        if(message == "pause"):
            aud_in.stop()
            websocket.send_text(f"Stream was paused")
        elif(message == "stop"):
            aud_in.close()
            websocket.send_text(f"Stream was terminated")
            return
        else:
            data = aud_in.play()
            print(data)

        await websocket.send_text(f"Invalid method:{message}")