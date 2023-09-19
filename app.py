from flask import Flask, jsonify
from src.speech2text.pipeline.recordnavigator import AudioRecorder
from flask import Flask, render_template, request, Response
from prediction.pipeline import PredictionPipeline
import uuid
from threading import Thread
import os
import json
import boto3
import time
import pandas as pd
from botocore.exceptions import ClientError
from summarizer import logger
from src.speech2text.pipeline.aws_ops import AWSTranscribe
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# AWS Configuration-----------------------------------------
AWS_ACCESS_KEY = "AKIAUDNY7G4FT2CYXZU6"
AWS_SECRET_KEY = "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"
AWS_REGION = "eu-central-1"
BUCKET_NAME = "dimo-transcribe-hubermanlab-podcasts"

ongoing_jobs = set()
recorder = None  # Global recorder instance
aws_transcriber = AWSTranscribe(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, BUCKET_NAME)

s3_client = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if 'file' is in the request's files part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # If the user does not select a file, the browser might
    # submit an empty file without a filename.
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file has the .mp3 extension
    if not file.filename.endswith('.mp3'):
        return jsonify({'error': 'Invalid file type'}), 400
    
#   Save the file to S3 bucket
    try:
        s3_client.upload_fileobj(file, BUCKET_NAME, file.filename)
    except ClientError as e:
        return jsonify({'error': f'Failed to upload file to S3: {str(e)}'}), 500
    job_name = aws_transcriber.start_transcription(file.filename)
    
    ongoing_jobs.add(job_name)
     # Ensure the directory exists

    return jsonify({'message': 'File uploaded to S3 successfully'+job_name}), 200

@app.route('/fetch_transcriptions', methods=['GET'])
def fetch_transcriptions():
    completed_transcriptions = list(aws_transcriber.wait_for_results(ongoing_jobs))

    # Clear ongoing jobs that are completed
    for job, _ in completed_transcriptions:
        ongoing_jobs.remove(job)

    # Convert the transcription results to some serializable format
    # serialized_transcriptions = [(job, df.to_dict()) for job, df in completed_transcriptions]
     # Extract only the transcripts
    serialized_transcriptions = [
        ( res['results']['transcripts'][0]['transcript']) for job, res in completed_transcriptions
    ]

    return jsonify(serialized_transcriptions)

predictor_pipeline = PredictionPipeline()

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

    """Return first the response and tie the predict_async to a thread"""
    Thread(target = predictor_pipeline.predict_async, args=(file_id, file)).start()
    # await predictor_pipeline.predict_async(file_id, file)

    return Response(
        "{\n\t\"id\": \"" +  file_id + "\"\n}",
        content_type='application/json',
        status=202,
    )

@app.route('/predict/<pred_id>', methods=['GET'])
def get_predict_content(pred_id):
    assert pred_id == request.view_args['pred_id']
    prediction = predictor_pipeline.get_prediction(pred_id)
    if not prediction:
        return Response(content_type='application/json', status=102)
    return prediction

@app.route('/start', methods=['Post'])
def get_data():
    global recorder
    if not recorder:
        recorder = AudioRecorder(record_seconds=10)
        recorder.start_audio()
        return jsonify({'message': 'Recording started'})
    else:
        return jsonify({'message': 'Recording is already in progress'})


@app.route('/stop', methods=['Post'])
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
    # app.run('0.0.0.0', port='8080', debug=True)
    app.run('0.0.0.0', port='8080')