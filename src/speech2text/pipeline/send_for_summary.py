from speech2text import logger
from speech2text.config.configuration import ConfigManager

class Summarizer:
    def __init__(self, config_manager: ConfigManager, summary_pipeline) -> None:
        self.config_manager = config_manager
        self.summary_pipeline = summary_pipeline

    def summarize(self, transcr_generator):
        for job_id, transcr in transcr_generator:
            logger.info(f'Receive transcription for {job_id} with value {transcr[:5]}')
            self.summary_pipeline.predict(transcr, job_id)