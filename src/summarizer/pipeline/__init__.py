from src.summarizer import logger
from src.summarizer.config.configuration import ConfigManager

from src.summarizer.pipeline.data_reader import DataReader
from src.summarizer.pipeline.model import ModelCreator
from src.summarizer.pipeline.trainer import ModelTrainer
from src.summarizer.pipeline.evaluate import ModelEvaluator
from src.summarizer.pipeline.log_model import MlFlowLogger

class SummarizerPipeline:
    def __init__(self) -> None:
        self.config_manager = ConfigManager()
        self._data_reader = DataReader(self.config_manager)
        self._model_creator = ModelCreator(self.config_manager)
        self._trainer = ModelTrainer(self.config_manager)
        self._evaluator = ModelEvaluator(self.config_manager)
        self._model_logger = MlFlowLogger(self.config_manager)

    def main(self):
        texts, reference_summaries = self._data_reader.main()
        pipe = self._model_creator.create_pipeline()
        pipe = self._trainer.train(pipe)

        scores = self._evaluator.evaluate(pipe, texts, reference_summaries)
        self._model_logger.log_model(pipe, scores)

if __name__ == '__main__':
    pipeline = SummarizerPipeline()
    logger.info('Start summarizing pipeline...')
    pipeline.main()
    logger.info('Summarization finished.')