from speech2text import logger
from speech2text.config.configuration import ConfigManager
import boto3
import os
import pandas as pd
import time
from pathlib import Path

class ResultWait:
    def __init__(self, config_manager: ConfigManager, transcribe_client) -> None:
        self.config_manager = config_manager
        if transcribe_client:
            self.transcribe_client = transcribe_client
        else:
            self.transcribe_client = boto3.client('transcribe',
                aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY_ID'],
                region_name = os.environ['AWS_REGION'])
            logger.info(f"""Create transcribe Boto client with credentials: ACCESS_KEY {os.environ['AWS_ACCESS_KEY_ID'][:2]}
                    \n and SECRET_ACCESS_KEY {os.environ['AWS_SECRET_ACCESS_KEY_ID'][:2]} \n in region {os.environ['AWS_REGION']} """)
    
    def wait_for_results(self, job_generator):
        jobs = {job for job in job_generator}
        completed_jobs = set()
        while len(jobs) > len(completed_jobs):
            for job in {j for j in jobs if j not in completed_jobs }:
                result = self.transcribe_client.get_transcription_job(TranscriptionJobName=job)
                status = result['TranscriptionJob']['TranscriptionJobStatus']
                print(f'Status: {status} for job {job}')
                if status == 'FAILED':
                    failure_reason = result['TranscriptionJob']['FailureReason']
                    print(f'Job with name {job} failed with {failure_reason}')
                    completed_jobs.add(job)
                if status == 'COMPLETED':
                    print(f'Job with name {job} completed')
                    completed_jobs.add(job)
                    res_uri = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
                    read_df = pd.read_json(res_uri)
                    read_df.to_csv(Path(self.config_manager.config.transciptions.aws_results, job + '.csv'))
                    logger.info(f'Data received with transcribtion:\n{read_df.head()}')
                    result = read_df.iloc[-1]['results'][0]['transcript']
                    yield (job, result)
            time.sleep(10)
