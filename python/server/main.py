from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from urllib.parse import unquote 
import sys

sys.path.append('../')

from scraper.stream import getWav
from recorder.recorder import Recorder

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # can alter with time
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/getwav/")
def read_item(url: str):
    url = unquote(unquote(url))
    getWav(url)
    return {"url": url}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    aud_in = Recorder('audio.wav')
    status = "stop"
    while True:

        try:
            message = await websocket.receive_text()
            
            async def run_thread_process():
                while status == "play" and websocket.client_state not in [0, 2]:
                    try:
                        data = aud_in.play()
                        await websocket.send_json(data)
                    except:
                        print('Stream was terminated, data not sent')
                        return
                    
                if status == "pause":
                    aud_in.stop()                    
                elif status == "stop":
                    aud_in.close()
                    
            if(message == "pause"):
                status = "pause"
                await websocket.send_text(f"Stream was paused")
                
            elif(message == "stop"):
                status = "stop"
                await websocket.send_text(f"Stream was terminated")
                await websocket.close()
            
            elif(message == "play"):
                status = "play"
                loop = asyncio.get_running_loop()
                loop.run_in_executor(None, lambda: asyncio.run(run_thread_process()))
                await websocket.send_text(f"Stream was started")
                
            else:
                await websocket.send_text(f"Invalid method:{message}")
        
        except:
            aud_in.stop()
            aud_in.close()
            status = "stop"
            print(f"fatal error with stream, connection terminated")
            return
