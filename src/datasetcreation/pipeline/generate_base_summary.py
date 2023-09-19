import pandas as pd
from src.datasetcreation.config.configuration import ConfigManager
from pathlib import Path
from src.datasetcreation.constants import CSV_DELIMITER
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
from ensure import ensure_annotations
from src.datasetcreation import logger

STAGE_NAME = 'Preprocess conversation'

class BaseSummaryGenerator:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def main(self):
        dataset_path = Path(self.config_manager.config.dataset.base_dir, self.config_manager.config.dataset.file_name)
        dataframe = pd.read_csv(dataset_path, sep=CSV_DELIMITER)
        pipeline = self._create_pipeline()

        dataframe['summary'] = self._generate_summary(pipeline, dataframe['conversation'])

        dataframe.to_csv(dataset_path, sep=CSV_DELIMITER)

    def _create_pipeline(self):
        tokenizer = BartTokenizer.from_pretrained(self.config_manager.config.summarization.tokenizer_name)
        model = BartForConditionalGeneration.from_pretrained(self.config_manager.config.summarization.model_name)

        return pipeline('summarization', model=model, tokenizer=tokenizer, framework="pt", truncation=True)
    
    @ensure_annotations
    def _generate_summary(self, pipeline, texts: pd.Series):
        min_len = self.config_manager.config.summarization.min_length
        max_len = self.config_manager.config.summarization.max_length
        def sum_text(t):
            try:
                return pipeline(t, max_length=max_len, min_length=min_len)[0]
            except Exception as e:
                logger.error(f'Error summarizing {t}, {e}')
                return {'summary_text': None}
        summaries = [sum_text(t) for t in texts.to_list()]
        return [summary['summary_text'] for summary in summaries]
    
if __name__ == '__main__':
    config_manager = ConfigManager()
    stage = BaseSummaryGenerator(config_manager)

    stage.main()