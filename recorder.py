import pyaudio
import soundfile as sf
import numpy as np
import wave
import time

class Recorder:

    def __init__(self, file):
        self.wf = wave.open(file, "rb")
        self.samplerate = 44100
        self.pyaudio = pyaudio.PyAudio()
        self.chunk = 1024
        self.stream =  self.pyaudio.open(
            format = pyaudio.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True)
        self.frames = np.array([], dtype=np.int16)
        
    def play(self):
        if(self.stream.is_stopped):
            self.stream.start_stream()
        data = self.wf.readframes(self.chunk)
        self.stream.write(data) 
        self.frames = np.concatenate((self.frames, np.frombuffer(data, dtype=np.int16)))


    def stop(self):
        if self.stream:
            self.stream.stop_stream()

    def writeAudio(self, OUTPUT_FILE_NAME):
        self.stream.close()
        self.pyaudio.terminate()
        sf.write(file=OUTPUT_FILE_NAME, data=self.frames, samplerate=self.samplerate)

if __name__ == '__main__':
    recorder = Recorder()