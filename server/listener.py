import asyncio
from websockets.server import serve
import sys
import json

sys.path.append('../')

from scraper.stream import getWav
from recorder.recorder import Recorder

# getWav("https://www.youtube.com/watch?v=_W88oVKhNW0&ab_channel=Geoxor")
aud_in = Recorder('audio.wav')

async def echo(websocket):
    async for message in websocket:
        if(message == "play"):
            data = await aud_in.play()
            await websocket.send(json.dumps(data))
        elif(message == "stop"):
            await aud_in.stop()
            await websocket.send(message)
        else:
            print(message)
            await websocket.send("invalid input")

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())