import asyncio
from websockets.server import serve
import sys
import json

sys.path.append("../")

from scraper.stream import getWav
from recorder.recorder import Recorder

# getWav("https://www.youtube.com/watch?v=ZrlZsEeS2AQ&ab_channel=Zenkaso")

aud_in = Recorder("audio.wav")


async def echo(websocket):
    global aud_in
    async for message in websocket:
        if message == "play":
            data = await aud_in.play()
            await websocket.send(json.dumps(data))
        elif message == "stop":
            await aud_in.stop()
            await websocket.send(message)
        elif message == "Vol":
            aud_in.eq["vol"] = int(float(await websocket.recv()))
        else:
            aud_in = Recorder("audio.wav")
            await websocket.send("closing stream")


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
