import pyaudio
import soundfile as sf
import numpy as np
import wave
import time

class Recorder:

    def __init__(self):
        self.samplerate = 44100
        self.pyaudio = pyaudio.PyAudio()
        self.chunk = 4096
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
        data = self.stream.read(self.chunk)
        print(data)
        self.frames = np.concatenate((self.frames, np.frombuffer(data, dtype=np.int16)))


    def stop(self):
        if self.stream:
            self.stream.stop_stream()

    def writeAudio(self, OUTPUT_FILE_NAME):
        self.stream.close()
        self.pyaudio.terminate()
        sf.write(file=OUTPUT_FILE_NAME, data=self.frames*10, samplerate=self.samplerate)

if __name__ == '__main__':
    recorder = Recorder()