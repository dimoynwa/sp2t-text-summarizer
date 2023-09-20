from src.speech2text import logger
from src.speech2text.pipeline.read_content import FileRead
from src.speech2text.pipeline.save_file import S3Saver
from src.speech2text.pipeline.aws_transcribe import TranscriptionJob
from src.speech2text.pipeline.aws_transcribe_results import ResultWait
from src.speech2text.pipeline.send_for_summary import Summarizer
from src.speech2text.config.configuration import ConfigManager
from src.speech2text.utils.common import create_directories

import boto3
import os

class Speech2TextPipeline:
    def __init__(self, summarizer_pipeline) -> None:
        self.config_manager = ConfigManager()
        create_directories([self.config_manager.config.transciptions.base_dir,
                            self.config_manager.config.transciptions.audio_files_dir,
                            self.config_manager.config.transciptions.aws_results])
        self.transcribe_client = boto3.client('transcribe',
            aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY_ID'],
            region_name = os.environ['AWS_REGION'])
        logger.info(f"""Created transcribe Boto client with credentials: ACCESS_KEY {os.environ['AWS_ACCESS_KEY_ID'][:2]}
            \n and SECRET_ACCESS_KEY {os.environ['AWS_SECRET_ACCESS_KEY_ID'][:2]} \n in region {os.environ['AWS_REGION']} """)
        self._file_read = FileRead(self.config_manager)
        self._s3_saver = S3Saver(self.config_manager)
        self._transcr_job = TranscriptionJob(self.config_manager, self.transcribe_client)
        self._result_wait = ResultWait(self.config_manager, self.transcribe_client)
        self._summarizer = Summarizer(self.config_manager, summarizer_pipeline)

    def transcribe(self, file_id, file_content):
        self._summarizer.summarize(self._result_wait.wait_for_results(
            self._transcr_job.send_for_transcribe(self._s3_saver.save_to_s3(self._file_read.main(file_id, file_content)))
        ))