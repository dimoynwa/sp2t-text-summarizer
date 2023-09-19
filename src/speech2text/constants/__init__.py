from pathlib import Path
from flask import app

import pyaudio

CONFIG_FILE_PATH = Path('config/prediction.yml')
# The folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio
RATE = 20000  # Sample rate (samples per second)
RECORD_SECONDS = 60  # Duration of recording