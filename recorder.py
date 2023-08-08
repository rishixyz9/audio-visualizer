import pyaudio
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
import math

class Recorder:

    def __init__(self):
        self.samplerate = 44100
        self.pyaudio = pyaudio.PyAudio()
        self.chunk = 4069
        self.stream =  self.pyaudio.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = self.samplerate,
            input = True,
            output=True,
            frames_per_buffer=self.chunk)
        self.frames = np.array([], dtype=np.int16)
        
    def play(self):
        if(self.stream.is_stopped):
            self.stream.start_stream()
            
        data = np.frombuffer(self.stream.read(self.chunk, exception_on_overflow=False), dtype=np.int16)
        self.frames = np.concatenate((self.frames, data))

        fft = np.fft.fft(data) / len(data)
        freqs = np.abs(np.fft.fftfreq(len(data)))

        return (freqs * self.samplerate, np.abs(fft))

    def stop(self):
        if self.stream:
            self.stream.stop_stream()

    def writeAudio(self, OUTPUT_FILE_NAME):
        self.stream.close()
        self.pyaudio.terminate()
        sf.write(file=OUTPUT_FILE_NAME, data=self.frames, samplerate=self.samplerate)

if __name__ == '__main__':
    recorder = Recorder()