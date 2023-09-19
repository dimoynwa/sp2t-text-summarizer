import boto3
import time

import pandas as pd

class AWSTranscribe:
    def __init__(self, access_key, secret_key, region, bucket_name):
        self.s3_client = boto3.client('s3', aws_access_key_id=access_key, 
                                      aws_secret_access_key=secret_key, region_name=region)
        self.transcribe_client = boto3.client('transcribe', aws_access_key_id=access_key, 
                                              aws_secret_access_key=secret_key, region_name=region)
        self.bucket_name = bucket_name

    def upload_to_s3(self, file_obj, file_name):
        self.s3_client.upload_fileobj(file_obj, self.bucket_name, file_name)
        
    def start_transcription(self, file_name):
        job_name = file_name.replace(".mp3", "") + str(round(time.time()*1000))
        file_uri = 's3://' + self.bucket_name + '/' + file_name
        print('Start transcribe job for ', file_uri, 'job name:', job_name)
        # file_format = filename.split('.')[-1]

        self.transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_uri},
            MediaFormat='mp3',
            LanguageCode='en-US')
        return job_name
    
    def get_transcription(self, job_name):
        while True:
            result = self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            status = result['TranscriptionJob']['TranscriptionJobStatus']
            if status in ['COMPLETED', 'FAILED']:
                break
            time.sleep(10)

        if status == 'COMPLETED':
            return result['TranscriptionJob']['Transcript']['TranscriptFileUri']
        else:
            return None
            
    def wait_for_results(self, jobs_list):
        jobs = set(jobs_list)
        print(f'Jobs:  {jobs}')
        completed_jobs = set()
        while len(jobs) > len(completed_jobs):
            for job in {j for j in jobs if j not in completed_jobs}:
                result = self.transcribe_client.get_transcription_job(TranscriptionJobName=job)
                status = result['TranscriptionJob']['TranscriptionJobStatus']
                print(f'Status: {status} for job {job}')
                
                if status == 'FAILED':
                    print(f'Job with name {job} failed')
                    completed_jobs.add(job)
                elif status == 'COMPLETED':
                    print(f'Job with name {job} completed')
                    completed_jobs.add(job)
                    res_uri = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
                    transcription_result = pd.read_json(res_uri)
                    yield (job, transcription_result)
            time.sleep(10)
