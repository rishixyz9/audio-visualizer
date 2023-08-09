import pyaudio
import soundfile as sf
import numpy as np
import wave

class Recorder:

    def __init__(self, file):
        self.wf = wave.open(file, 'rb')
        self.samplerate = self.wf.getframerate()
        self.pyaudio = pyaudio.PyAudio()
        self.chunk = 4069
        self.stream =  self.pyaudio.open(
            format = self.pyaudio.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.samplerate,
            output=True,
            frames_per_buffer=self.chunk)
        self.frames = np.array([], dtype=np.int16)
        
    def play(self):
        if(self.stream.is_stopped):
            self.stream.start_stream()
            
        data = self.wf.readframes(self.chunk)
        self.stream.write(data)
        
        data = np.frombuffer(data, dtype=np.int16)
        self.frames = np.concatenate((self.frames, data))
        

        fft = np.fft.fft(data) / len(data) #scale data down
        freqs = np.abs(np.fft.fftfreq(len(data))) #get frequencies from len of buffer

        #retrrns the scaled frequencies and magnitude of their corresponding amplitudes
        return (freqs * self.samplerate, np.abs(fft))

    def stop(self):
        if self.stream:
            self.stream.stop_stream()

    def close(self, write=False, OUTPUT_FILE_NAME=None):
        self.stream.close()
        self.pyaudio.terminate()
        if write:
            sf.write(file=OUTPUT_FILE_NAME, data=self.frames, samplerate=self.samplerate)

        

if __name__ == '__main__':
    recorder = Recorder()