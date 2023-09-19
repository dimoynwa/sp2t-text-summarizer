from prediction import logger
from prediction.config.configuration import ConfigManager
from prediction.utils.common import create_directories
import mlflow
from ensure import ensure_annotations
import os

class Predictor:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        create_directories([self.config_manager.config.predictions.base_dir])
        mlflow.set_tracking_uri(self.config_manager.config.mlflow.tracking_uri)

        os.environ['MLFLOW_TRACKING_USERNAME'] = 'dimoynwa'
        os.environ['MLFLOW_TRACKING_PASSWORD'] = 'b438e26f2c75bb68347e97b2096330de3ad1e94f'

        logger.info(f"MLFLOW_TRACKING_USERNAME: {os.environ['MLFLOW_TRACKING_USERNAME'][:2]}")
        logger.info(f"MLFLOW_TRACKING_PASSWORD: {os.environ['MLFLOW_TRACKING_PASSWORD'][:2]}")
        
        logger.info(f'MLFlow initialized with tracking uri: {self.config_manager.config.mlflow.tracking_uri}')
        self.pyfunc_loaded = mlflow.pyfunc.load_model(self.config_manager.config.mlflow.model_uri)

    @ensure_annotations
    def predict(self, text: str) -> list:
        logger.info(f'Predicting with model {self.config_manager.config.mlflow.model_uri} for text: \n{text}')
        # inference_config will be applied
        result = self.pyfunc_loaded.predict(text)
        return result
    
    def predict_generator(self, generator) -> None:
        for file_id, content in generator:
            prediction = self.predict(content)
            yield file_id, prediction

if __name__ == '__main__':
    cm = ConfigManager()
    predictor = Predictor(cm)

    text = """
    Tim: Hi, what's up?
    Kim: Bad mood tbh, I was going to do lots of stuff but ended up procrastinating
    Tim: What did you plan on doing?
    Kim: Oh you know, uni stuff and unfucking my room
    Kim: Maybe tomorrow I'll move my ass and do everything
    Kim: We were going to defrost a fridge so instead of shopping I'll eat some defrosted veggies
    Tim: For doing stuff I recommend Pomodoro technique where u use breaks for doing chores
    Tim: It really helps
    Kim: thanks, maybe I'll do that Tim: I also like using post-its in kaban style
    """

    prediction = predictor.predict(text)
    print(f'Prediction: {prediction}')