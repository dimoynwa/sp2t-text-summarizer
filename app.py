from flask import Flask, jsonify
from speech2text.pipeline.recordnavigator import AudioRecorder
from flask import Flask, render_template, request, Response
from prediction.pipeline import PredictionPipeline
from speech2text.pipeline import Speech2TextPipeline
import uuid
from threading import Thread
import os

APPLICATION_JSON = 'application/json'

app = Flask(__name__)
recorder = None  # Global recorder instance
predictor_pipeline = PredictionPipeline()
speech2text_pipeline = Speech2TextPipeline(predictor_pipeline)

@app.route('/predict', methods=['POST']) 
def predict():
    text = request.json
    print(text)
    prediction = predictor_pipeline.predict(text['text'])
    return prediction

@app.route('/predict/file', methods=['POST'])
async def predict_file():
    file = request.files['file']

    file_id = str(uuid.uuid4())

    extension = file.filename.split(".")[-1]

    """Return first the response and tie the predict_async to a thread"""
    if extension == 'txt':
        Thread(target = predictor_pipeline.predict_async, args=(file_id, file.read())).start()
    elif extension == 'wav':
        file.save(file_id + '.wav')
        Thread(target= speech2text_pipeline.transcribe, args=(file_id, file.read())).start()
    else:
        return Response("{\n\t\"error\": \"" +  f'File Extention {extension} not supporter' + "\"\n}",
                        content_type=APPLICATION_JSON, status=400)
    # await predictor_pipeline.predict_async(file_id, file)

    return Response(
        "{\n\t\"id\": \"" +  file_id + "\"\n}",
        content_type=APPLICATION_JSON,
        status=202,
    )

@app.route('/predict/<pred_id>', methods=['GET'])
def get_predict_content(pred_id):
    assert pred_id == request.view_args['pred_id']
    prediction = predictor_pipeline.get_prediction(pred_id)
    if not prediction:
        return Response('{ "status": "NOT_PROCESSED_YET" }',
            content_type=APPLICATION_JSON, status=102)
    return jsonify({'prediction': prediction})


@app.route('/start', methods=['GET'])
def get_data():
    global recorder
    if not recorder:
        recorder = AudioRecorder(speech2text_pipeline, record_seconds=10)
        recorder.start_audio()
        return jsonify({'message': 'Recording started'})
    else:
        return jsonify({'message': 'Recording is already in progress'})


@app.route('/stop', methods=['GET'])
def stop_record():
    global recorder
    if recorder:
        file_id = str(uuid.uuid4())

        recorder.stop_audio()
        recorder.save_audio(file_id)
        recorder = None
        
        return jsonify({'id': file_id ,'message': 'Recording stopped'})
    else:
        return jsonify({'message': 'No recording in progress'})

if __name__ == '__main__':
    # app.run('0.0.0.0', port='8080', debug=True)
    app.run('0.0.0.0', port='8080')