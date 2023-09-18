from flask import Flask, render_template, request, Response
from prediction.pipeline import PredictionPipeline
import uuid

app = Flask(__name__)

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
    
    await predictor_pipeline.predict_async(file_id, file)

    return Response(
        "{'id': \"" +  file_id + "\"}",
        content_type='application/json',
        status=202,
    )

if __name__ == '__main__':
    # app.run('0.0.0.0', port='8080', debug=True)
    app.run('0.0.0.0', port='8080')