from src.summarizer import logger
from src.summarizer.config.configuration import ConfigManager

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

class ModelCreator:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def create_pipeline(self):
        model_name = self.config_manager.config.model.name
        padding = self.config_manager.config.model.padding
        truncation = self.config_manager.config.model.truncation

        tokenizer = AutoTokenizer.from_pretrained(model_name, padding=padding)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        pipe = pipeline('summarization', model=model, tokenizer=tokenizer, truncation=truncation)
        
        logger.info(f'Created model and tokenizer for name {model_name} with truncation {truncation}')

        return pipe
    
if __name__ == '__main__':
    cm = ConfigManager()
    model_creator = ModelCreator(cm)
    model_creator.create_pipeline()