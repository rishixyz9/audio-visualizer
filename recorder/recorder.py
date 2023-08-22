import pyaudio
import soundfile as sf
import numpy as np
import wave
import json

class Recorder:

    def __init__(self, file):
        self.wf = wave.open(file, 'rb')
        self.samplerate = self.wf.getframerate()
        self.pyaudio = pyaudio.PyAudio()
        self.chunk = 4096
        self.stream =  self.pyaudio.open(
            format = self.pyaudio.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.samplerate,
            output=True,
            frames_per_buffer=self.chunk)
        self.frames = np.array([], dtype=np.int16)
        
    async def play(self):
        if(self.stream.is_stopped):
            self.stream.start_stream()
            
        data = self.wf.readframes(self.chunk)
        self.stream.write(data)
        
        if(data):
            data = np.frombuffer(data, dtype=np.int16)
            self.frames = np.concatenate((self.frames, data))
            

            fft = np.abs(np.fft.rfft(data) / len(data)) #scale data down
            freqs = np.abs(np.fft.rfftfreq(len(data))) #get frequencies from len of buffer

            #returns the scaled frequencies and magnitude of their corresponding amplitudes
            buckets = self.flatten(freqs * self.samplerate, fft)

            return (list(range(1, len(buckets.keys())+1)), list(buckets.values()))
            
        return ([0], [0])

    async def stop(self):
        if self.stream:
            self.stream.stop_stream()

    async def close(self, write=False, OUTPUT_FILE_NAME=None):
        self.stream.close()
        self.pyaudio.terminate()
        if write:
            sf.write(file=OUTPUT_FILE_NAME, data=self.frames, samplerate=self.samplerate)

    def flatten(self, freqs, fft):
        cur = 16
        # buckets = {0:0, 8:0, 16:0, 38:0, 60:0, 155:0, 250:0, 375:0, 500:0, 1250:0, 2000:0, 3000:0, 4000:0, 6000:0, 8000:0}
        buckets = {0:0}
        while(cur < 20000):
            buckets[int(cur)] = 0
            cur *= 2**(4/12)

        right = len(buckets.keys())-1

        for i in range(len(freqs), 0, -1):
            bucket = list(buckets.keys())[right]
            while(freqs[i-1] < bucket):
                right -= 1
                bucket = list(buckets.keys())[right]
            
            buckets[bucket] += fft[i-1]
            if(buckets[bucket] != 0):
                buckets[bucket] /= 2
            buckets[bucket] %= 1000
        return buckets



        

if __name__ == '__main__':
    recorder = Recorder()