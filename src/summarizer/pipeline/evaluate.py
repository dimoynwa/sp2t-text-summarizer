from src.summarizer import logger
from src.summarizer.config.configuration import ConfigManager
from bert_score import score

from src.summarizer.pipeline.data_reader import DataReader
from src.summarizer.pipeline.model import ModelCreator
from src.summarizer.pipeline.trainer import ModelTrainer

class ModelEvaluator:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def evaluate(self, pipe, texts, reference_summaries):
        logger.info(f'Generating summaries for {len(texts)} texts...')
        outputs = pipe(texts, max_length=self.config_manager.config.model.max_length, min_length=self.config_manager.config.model.min_length, \
                        truncation=self.config_manager.config.model.truncation)
        output_texts = [sum['summary_text'] for sum in outputs]

        logger.info(f'Generated {len(output_texts)} summaries')

        logger.info('Calculating P, R and F1 scores...')
        P, R, F1 = score(output_texts, reference_summaries, lang="en", verbose=True)
        logger.info(f'Scores:\nP: {P.mean()}\nR: {R.mean()}\nF1: {F1.mean()}')
        scores = {'P': P.mean(), 'R': R.mean(), 'F1_score': F1.mean()}
        return scores
    
if __name__ == '__main__':
    cm = ConfigManager()
    data_reader = DataReader(cm)
    model_creator = ModelCreator(cm)
    trainer = ModelTrainer(cm)
    evaluator = ModelEvaluator(cm)

    texts, reference_summaries = data_reader.main()
    pipe = model_creator.create_pipeline()
    pipe = trainer.train(pipe)

    scores = evaluator.evaluate(pipe, texts, reference_summaries)
    logger.info(f'Calculated scores: {scores}')
