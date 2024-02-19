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
        self.eq = {"vol": 50}

    # returns a tuple of the frequencies and their corresponding amplitudes
    async def play(self):
        # if the stream is stopped, start it
        if self.stream.is_stopped:
            self.stream.start_stream()

        # read the next chunk of data
        data = self.wf.readframes(self.chunk)
        volume_factor = self.eq["vol"] / 100  # Convert volume percentage to a factor
        if data:
            data = np.frombuffer(data, dtype=np.int16)

            adjusted_data = data * volume_factor  # Apply volume adjustment
            adjusted_data = adjusted_data.astype(
                np.int16
            ).tobytes()  # Convert adjusted data back to bytes for playback
            self.stream.write(adjusted_data)  # write the adjusted data to the stream

            self.frames = np.concatenate((self.frames, data))

            fft = np.abs(np.fft.rfft(data) / len(data))  # scale data down
            freqs = np.abs(
                np.fft.rfftfreq(len(data))
            )  # get frequencies from len of buffer

            # returns the scaled frequencies and magnitude of their corresponding amplitudes
            buckets = self.flatten(freqs * self.samplerate, fft)

            return (
                list(buckets.keys()),
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

        # buckets = {
        #     0: 0,
        #     16: 0,
        #     60: 0,
        #     250: 0,
        #     500: 0,
        #     2000: 0,
        #     4000: 0,
        #     6000: 0,
        #     20000: 0,
        # }

        cur = 16
        buckets = {0: 0}
        # creates buckets up to 20k since that is the highest frequency humans can hear
        while cur < 20000:
            buckets[int(cur)] = 0
            cur *= 2 ** (2 / 12)

        right = len(buckets.keys()) - 1

        # combs through the frequencies and puts them in the correct bucket
        for i in range(len(freqs) - 1, 0, -1):
            bucket = list(buckets.keys())[right]
            # iterates until the a bucket is found that is less than the current frequency
            while freqs[i - 1] < bucket:
                right -= 1
                bucket = list(buckets.keys())[right]

            # takes the average of a bucket if there are multiple frequencies in it
            # buckets[bucket] = (
            #     fft[i - 1]
            #     if buckets[bucket] == 0
            #     else (buckets[bucket] + fft[i - 1]) / 2
            # )

            amplitude_in_db = 20 * np.log10(max(fft[i], 1))  # Use 1e-10 to avoid log(0)

            # Update bucket with amplitude in dB, averaging if necessary
            if buckets[bucket] == 0:
                buckets[bucket] = amplitude_in_db
            else:
                buckets[bucket] = (buckets[bucket] + amplitude_in_db) / 2

            # buckets[bucket] = min(buckets[bucket], 3000)  # clamps max amplitude to 5000

        return buckets


if __name__ == "__main__":
    recorder = Recorder()
