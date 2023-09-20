from pathlib import Path
from flask import app

import pyaudio

CONFIG_FILE_PATH = Path('config/speech2text.yml')
MP3_FILE_EXT = '.mp3'
# The folder to save uploaded files
UPLOAD_FOLDER = 'uploads'

CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio
RATE = 20000  # Sample rate (samples per second)
RECORD_SECONDS = 60  # Duration of recording