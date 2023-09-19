from flask import Flask, jsonify
from speech2text.pipeline.recordnavigator import AudioRecorder

app = Flask(__name__)
recorder = None  # Global recorder instance

@app.route('/start', methods=['GET'])
def get_data():
    global recorder
    if not recorder:
        recorder = AudioRecorder(record_seconds=10)
        recorder.start_audio()
        return jsonify({'message': 'Recording started'})
    else:
        return jsonify({'message': 'Recording is already in progress'})


@app.route('/stop', methods=['GET'])
def stop_record():
    global recorder
    if recorder:
        recorder.stop_audio()
        recorder.save_audio()
        recorder = None
        
        return jsonify({'message': 'Recording stopped'})
    else:
        return jsonify({'message': 'No recording in progress'})

if __name__ == '__main__':
    app.run(debug=True)
