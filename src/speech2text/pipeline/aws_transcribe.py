from src.speech2text import logger
from src.speech2text.config.configuration import ConfigManager
from src.speech2text.constants import MP3_FILE_EXT
import boto3
import os
from botocore.exceptions import ClientError

class TranscriptionJob:
    def __init__(self, config_manager: ConfigManager, transcribe_client) -> None:
        self.config_manager = config_manager
        self.bucket_name = config_manager.config.s3.bucket_name
        if transcribe_client:
            self.transcribe_client = transcribe_client
        else:
            self.transcribe_client = boto3.client('transcribe',
                aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY_ID'],
                region_name = os.environ['AWS_REGION'])
            logger.info(f"""Create transcribe Boto client with credentials: ACCESS_KEY {os.environ['AWS_ACCESS_KEY_ID'][:2]}
                    \n and SECRET_ACCESS_KEY {os.environ['AWS_SECRET_ACCESS_KEY_ID'][:2]} \n in region {os.environ['AWS_REGION']} """)

    def send_for_transcribe(self, file_id_gen):
        for file_id in file_id_gen:
            file_uri = 's3://' + self.bucket_name + '/' + file_id + '.wav'
            job_name = file_id
            logger.info('Start transcribe job for ', file_uri, 'job name:', job_name)
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': file_uri},
                MediaFormat = "wav",
                LanguageCode='en-US')
            yield job_name