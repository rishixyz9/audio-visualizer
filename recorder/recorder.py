import pyaudio
import soundfile as sf
import numpy as np
import wave
from struct import pack
import json


class Recorder:
    def __init__(self, file):
        self.wf = wave.open(file, "rb")
        self.samplerate = self.wf.getframerate()
        self.pyaudio = pyaudio.PyAudio()
        self.chunk = 4096
        self.stream = self.pyaudio.open(
            format=self.pyaudio.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.samplerate,
            output=True,
            frames_per_buffer=self.chunk,
        )
        self.frames = np.array([], dtype=np.int16)
        self.eq = {"vol": 100}

    # returns a tuple of the frequencies and their corresponding amplitudes
    async def play(self):
        # if the stream is stopped, start it
        if self.stream.is_stopped:
            self.stream.start_stream()

        # read the next chunk of data
        data = self.wf.readframes(self.chunk)
        self.stream.write(data)

        # if there is data, add it to the frames
        if data:
            data = np.frombuffer(data, dtype=np.int16)
            self.frames = np.concatenate((self.frames, data))

            fft = np.abs(np.fft.rfft(data) / len(data))  # scale data down
            freqs = np.abs(
                np.fft.rfftfreq(len(data))
            )  # get frequencies from len of buffer

            # returns the scaled frequencies and magnitude of their corresponding amplitudes
            buckets = self.flatten(freqs * self.samplerate, fft)

            return (
                list(range(1, len(buckets.keys()) + 1)),
                list(buckets.values()),
            )  # flattens the values into a visualizable representation and returns the frequencies and their corresponding amplitudes

        return ([0], [0])

    # stops the stream
    async def stop(self):
        if self.stream:
            self.stream.stop_stream()

    # closes the stream
    async def close(self, write=False, OUTPUT_FILE_NAME=None):
        self.stream.close()
        self.pyaudio.terminate()
        # writes the frames out if there is write has been set to true and there is an output file name
        if write and OUTPUT_FILE_NAME:
            sf.write(
                file=OUTPUT_FILE_NAME, data=self.frames, samplerate=self.samplerate
            )

    # flattens the frequencies into a visualizable representation
    def flatten(self, freqs, fft):
        cur = 16
        # buckets = {0:0, 8:0, 16:0, 38:0, 60:0, 155:0, 250:0, 375:0, 500:0, 1250:0, 2000:0, 3000:0, 4000:0, 6000:0, 8000:0} //old
        buckets = {0: 0}
        # creates buckets up to 20k since that is the highest frequency humans can hear
        while cur < 20000:
            buckets[int(cur)] = 0
            cur *= 2 ** (2 / 12)

        right = len(buckets.keys()) - 1

        # combs through the frequencies and puts them in the correct bucket
        for i in range(len(freqs), 0, -1):
            bucket = list(buckets.keys())[right]
            # iterates until the a bucket is found that is less than the current frequency
            while freqs[i - 1] < bucket:
                right -= 1
                bucket = list(buckets.keys())[right]

            # takes the average of a bucket if there are multiple frequencies in it
            buckets[bucket] = (
                fft[i - 1]
                if buckets[bucket] == 0
                else (buckets[bucket] + fft[i - 1]) / 2
            )
        return buckets


if __name__ == "__main__":
    recorder = Recorder()
