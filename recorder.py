import pyaudio
import soundfile as sf
import numpy as np
import time

class Recorder:

    def __init__(self):
        self.SAMPLE_RATE = 44100 
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None
        self.frames = np.array([], dtype=np.int16)

    def callback(self, in_data, frame_count, time_info, status):
        buffer = np.frombuffer(in_data, dtype=np.int16)
        self.frames = np.concatenate((self.frames, buffer*10))
        return (in_data, pyaudio.paContinue)
    
    def listen(self):
        self.stream =  self.pyaudio.open(format=pyaudio.paInt16,
                channels=1,
                rate=self.SAMPLE_RATE,
                input=True,
                frames_per_buffer=128,
                stream_callback=self.callback)
        self.stream.start_stream()


    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def writeAudio(self, OUTPUT_FILE_NAME):
        self.pyaudio.terminate()
        sf.write(file=OUTPUT_FILE_NAME, data=self.frames, samplerate=self.SAMPLE_RATE)


recorder = Recorder()

recorder.listen()
time.sleep(5)
recorder.stop()
recorder.writeAudio('out.wav')