import asyncio
from websockets.server import serve
import sys
import json

sys.path.append("../")

from scraper.stream import getWav
from recorder.recorder import Recorder

# https://www.youtube.com/watch?v=F4Ec98UJXfA&ab_channel=TOKYOPILL-Topic
# https://www.youtube.com/watch?v=GHoyX2eBSQM&list=RDMM&start_radio=1&ab_channel=Carthago-Topic
# https://www.youtube.com/watch?v=M-2YVBCayq4&list=RDMM&index=2&ab_channel=glaiveVEVO
# https://www.youtube.com/watch?v=Rs_kavGKeHI&ab_channel=draingang

getWav("https://www.youtube.com/watch?v=3rLjJ3tAbzo&ab_channel=piri%26tommy")

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
        elif message == "exit":
            await aud_in.stop()
            await aud_in.close()
            await websocket.close()
            break
        elif message == "Vol":
            aud_in.eq["vol"] = int(float(await websocket.recv()))
        else:
            aud_in = Recorder("audio.wav")
            await websocket.send("closing stream")


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
