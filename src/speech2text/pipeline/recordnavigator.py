import pyaudio
import wave
from threading import Thread

class AudioRecorder:
    def __init__(self, speech2text_pipeline, chunk=1024, audio_format=pyaudio.paInt16, channels=1, rate=20000, record_seconds=60):
        self.CHUNK = chunk
        self.FORMAT = audio_format
        self.CHANNELS = channels
        self.RATE = rate
        self.RECORD_SECONDS = record_seconds
        self.frames = []
        self.isrecording = False
        self.speech2text_pipeline = speech2text_pipeline
        self.audio = pyaudio.PyAudio()

    def _record_audio(self):
        self.stream = self.audio.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)

        while self.isrecording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    def start_audio(self):
        self.isrecording = True
        self.thread = Thread(target=self._record_audio)
        self.thread.start()

    def stop_audio(self):
        self.isrecording = False
        self.thread.join()  # Wait for the recording thread to finish
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_audio(self, file_id):
        with wave.open(file_id + '.wav', "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(self.frames))
            print(f"Recording saved to {file_id}.wav.")
        Thread(target = self.speech2text_pipeline.transcribe, args=(file_id, "")).start()
        
if __name__ == "__main__":
    recorder = AudioRecorder()
