from speech2text import logger
from speech2text.config.configuration import ConfigManager
from speech2text.constants import MP3_FILE_EXT
import boto3
import os
from botocore.exceptions import ClientError

class S3Saver:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        self.bucket_name = config_manager.config.s3.bucket_name
        self.s3_client = boto3.client('s3',
            aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY_ID'],
            region_name = os.environ['AWS_REGION'])
        logger.info(f"""Create s3 Boto client with credentials: ACCESS_KEY {os.environ['AWS_ACCESS_KEY_ID'][:2]}
                    \n and SECRET_ACCESS_KEY {os.environ['AWS_SECRET_ACCESS_KEY_ID'][:2]} \n in region {os.environ['AWS_REGION']} """)
        self.create_bucket()

    def save_to_s3(self, file_gen):
        for file_id, file_content in file_gen:

            logger.info(f'Saving file MP3 file with Id {file_id} to s3 bucket {self.bucket_name}')
            try:
                response = self.s3_client.upload_file(
                    file_id + '.wav',
                    self.bucket_name,
                    file_id + '.wav'
                )
                logger.info(f'Response from uploading {file_id}: {response}')
                yield file_id
            except ClientError as e:
                logger.error(f'ERROR uploading file with ID {file_id} to bucket {self.bucket_name}', e)

    def create_bucket(self):
        buckets_response = self.s3_client.list_buckets()
        for bucket in buckets_response['Buckets']:
            if bucket['Name'] == self.bucket_name:
                logger.info(f'Bucket with name {self.bucket_name} already exists. Skip creating')
            return True
        try:
            if os.environ['AWS_REGION'] is None:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            else:
                location = {'LocationConstraint': os.environ['AWS_REGION']}
                self.s3_client.create_bucket(Bucket=self.bucket_name,
                                    CreateBucketConfiguration=location)
        except ClientError as e:
            logger.error('Error creating bucket', e)
            return False
        return True