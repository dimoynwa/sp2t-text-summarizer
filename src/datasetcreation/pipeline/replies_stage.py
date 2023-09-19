from src.datasetcreation.config.configuration import ConfigManager
import requests
from ensure import ensure_annotations
from src.datasetcreation.utils.common import get_slack_auth_token
from src.datasetcreation.pipeline.conversations_stage import ConversationsStage
from src.datasetcreation import logger
import time

STAGE_NAME = "Fetch replies"

class RepliesStage:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    @ensure_annotations
    def main(self, conversations_generator):
        auth_token = get_slack_auth_token()
        for channel_id, ts in conversations_generator():
            url = self.config_manager.config.slack.replies_url.replace('{channel_id}', channel_id).replace('{ts}', ts)
            headers = {'Authorization': f'Bearer {auth_token}'}
            try:
                response = requests.get(url, headers=headers)
                yield channel_id, ts, response.json()
            except Exception as e:
                logger.error(f'Error calling {url}, {e}')
            time.sleep(1)

if __name__ == '__main__':
    config_manager = ConfigManager()
    conv_stage = ConversationsStage(config_manager)
    stage = RepliesStage(config_manager)
    for channel, ts, response in stage.main(conv_stage.main):
        logger.info(f'Channel and ts: {channel}, {ts} returns response {response}')