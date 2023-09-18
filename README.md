## Text summarization using Hugging face, MLFlow and Dagshub ##

set SLACK_OAUTH_USER_TOKEN=...
python -m spacy download en_core_web_sm
MLFLOW_TRACKING_URI=https://dagshub.com/dimoynwa/sp2t-text-summarizer.mlflow \
MLFLOW_TRACKING_USERNAME=****** \
MLFLOW_TRACKING_PASSWORD=******  \