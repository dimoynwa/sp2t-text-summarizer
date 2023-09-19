import pyaudio
import wave
import threading

class AudioRecorder:
    def __init__(self, chunk=1024, audio_format=pyaudio.paInt16, channels=1, rate=20000, record_seconds=60):
        self.CHUNK = chunk
        self.FORMAT = audio_format
        self.CHANNELS = channels
        self.RATE = rate
        self.RECORD_SECONDS = record_seconds
        self.frames = []
        self.isrecording = False
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
        self.thread = threading.Thread(target=self._record_audio)
        self.thread.start()

    def stop_audio(self):
        self.isrecording = False
        self.thread.join()  # Wait for the recording thread to finish
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_audio(self, output_filename="output.mp3"):
        with wave.open(output_filename, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(self.frames))
        print(f"Recording saved to {output_filename}.")
if __name__ == "__main__":
    recorder = AudioRecorder()
